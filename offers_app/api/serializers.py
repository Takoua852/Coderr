from rest_framework import serializers
from offers_app.models import Offer, OfferDetail


class OfferSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_details = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()
    min_price = serializers.ReadOnlyField()
    min_delivery_time = serializers.ReadOnlyField()

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
        super().__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and request.parser_context.get('kwargs', {}).get('pk'):
            self.fields.pop('user_details', None)

    def get_user_details(self, obj):
        user = obj.user
        profile = getattr(user, 'profile', None)
        return {
            'first_name': profile.first_name if profile else user.first_name or '',
            'last_name': profile.last_name if profile else user.last_name or '',
            'username': user.username or ''
        }

    def get_details(self, obj):
        request = self.context.get('request')
        return [
            {
                "id": detail.id,
                "url": request.build_absolute_uri(f"/api/offerdetails/{detail.id}/") if request else f"/offerdetails/{detail.id}/"
            }
            for detail in obj.details.all()
        ]


class OfferDetailSerializer(serializers.ModelSerializer):

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


class OfferCreateSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        request = self.context.get('request')
        offer = Offer.objects.create(user=request.user, **validated_data)

        if len(details_data) != 3:
            raise serializers.ValidationError(
                "Ein Offer muss genau 3 Details enthalten.")

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)

        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get( 'description', instance.description)
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
                    detail_instance = OfferDetail.objects.create(offer=instance, **detail_data )
                    continue

                for field, value in detail_data.items():
                    setattr(detail_instance, field, value)
                detail_instance.save()

        return instance

