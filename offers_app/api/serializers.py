from rest_framework import serializers
from offers_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the OfferDetail model.

    Converts OfferDetail instances to JSON and vice versa for API responses.
    """

    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type'
        ]


class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer for the Offer model.

    Includes nested user details and offer details, along with
    calculated fields for minimum price and delivery time.
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_details = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)
    

    class Meta:
        model = Offer
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time',
            'user_details'
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

    def get_details(self, obj):
        """
        Return a list of related offer details with URLs.

        Args:
            obj: Offer instance

        Returns:
            List of dictionaries containing detail id and API URL.
        """
        request = self.context.get('request')
        return [
            {
                "id": detail.id,
                "url": request.build_absolute_uri(f"/api/offerdetails/{detail.id}/") if request else f"/offerdetails/{detail.id}/"
            }
            for detail in obj.details.all()
        ]

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
        details_data = validated_data.pop('details')
        request = self.context.get('request')

        if len(details_data) != 3:
            raise serializers.ValidationError(
                "An offer must contain exactly 3 details.")

        offer = Offer.objects.create(user=request.user, **validated_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer

    def to_representation(self, instance):
        """
        Use the standard OfferSerializer for the response representation.
        """
        return OfferSerializer(instance, context=self.context).data

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
                    continue
                try:
                    detail_instance = instance.details.get(
                        offer_type=offer_type)
                except OfferDetail.DoesNotExist:
                    detail_instance = OfferDetail.objects.create(
                        offer=instance, **detail_data)
                    continue

                for field, value in detail_data.items():
                    setattr(detail_instance, field, value)
                detail_instance.save()

        return instance
