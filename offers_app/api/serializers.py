from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from django.db.models import Min


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the OfferDetail model.

    Converts OfferDetail instances to JSON and vice versa for API responses.
    """
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days',
                  'price', 'features', 'offer_type'
                  ]


class OfferDetailUrlSerializer(serializers.ModelSerializer):
    """
    Serializer for OfferDetail that includes the API URL.

    Converts OfferDetail instances to JSON with an additional URL field.
    """
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f"/api/offerdetails/{obj.id}/") if request else f"/offerdetails/{obj.id}/"


class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer for the Offer model.

    Includes nested user details and offer details, along with
    calculated fields for minimum price and delivery time.
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_details = serializers.SerializerMethodField()
    details = OfferDetailUrlSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description', 'created_at',
            'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details'
        ]

    def __init__(self, *args, **kwargs):
        """
        Modify serializer fields based on context.

        Removes 'user_details' if the serializer is used for a single object (detail view)
        to avoid redundant data.
        """
        super().__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and request.parser_context.get('kwargs', {}).get('pk'):
            self.fields.pop('user_details', None)

    def get_user_details(self, obj):
        """
        Return nested user information.

        Args:
            obj: Offer instance

        Returns:
            Dictionary containing first_name, last_name, and username of the user.
        """
        user = obj.user
        profile = getattr(user, 'profile', None)
        return {
            'first_name': profile.first_name if profile else user.first_name or '',
            'last_name': profile.last_name if profile else user.last_name or '',
            'username': user.username or ''
        }

    def get_min_price(self, obj):
        """
        Return the minimum price from related OfferDetail objects.
        """
        return obj.details.aggregate(min_price=Min('price'))['min_price'] or 0

    def get_min_delivery_time(self, obj):
        """
        Return the minimum delivery time from related OfferDetail objects.
        """
        return obj.details.aggregate(min_delivery_time=Min('delivery_time_in_days'))['min_delivery_time'] or 0


class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Offer instances with nested OfferDetails.

    Ensures that each offer contains exactly 3 details and handles nested creation
    and updating of related OfferDetail instances.
    """
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def validate_details(self, value):
        request = self.context.get('request')
        if request and request.method == 'POST':
            if len(value) != 3:
                raise serializers.ValidationError(
                    "An offer must contain exactly 3 details."
                )
            
        offer_types = [d.get('offer_type') for d in value]
        if sorted(offer_types) != sorted([choice[0] for choice in OfferDetail.OFFER_TYPE_CHOICES]):
            raise serializers.ValidationError(
                "Each offer must have exactly one Basic, one Standard, and one Premium detail."
            )

        return value

    def create(self, validated_data):
        """
        Create a new Offer instance along with its nested details.

        Args:
            validated_data: Validated data from the request

        Returns:
            The newly created Offer instance

        Raises:
            serializers.ValidationError: If the offer does not contain exactly 3 details
        """
        details_data = validated_data.pop('details',[])
        request = self.context.get('request')

        offer = Offer.objects.create(user=request.user, **validated_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer


class OfferUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Offer instances without nested details.

    Allows updating only the main Offer fields.
    
    """
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']
    
    def update(self, instance, validated_data):
        """
        Update an existing Offer instance and its nested OfferDetails.

        Args:
            instance: Offer instance to update
            validated_data: Validated data from the request

        Returns:
            The updated Offer instance
        """
        details_data = validated_data.pop('details', None)

        instance.title = validated_data.get('title', instance.title)
        image = validated_data.get('image', None)
        if image is not None:
            instance.image = image
        instance.description = validated_data.get(
            'description', instance.description)
        instance.save()

        if details_data:
            for detail_data in details_data:
                offer_type = detail_data.get('offer_type')
                if not offer_type:
                    raise serializers.ValidationError({
                    "details": "offer_type is required for each detail."
                })

                try:
                    detail_instance = instance.details.get(offer_type=offer_type)
                except OfferDetail.DoesNotExist:
                    detail_instance = OfferDetail.objects.create(offer=instance, **detail_data)
                    continue

            for field, value in detail_data.items():
                if field != 'offer_type':
                    setattr(detail_instance, field, value)
            detail_instance.save() 

        return instance
    

    
