from rest_framework import serializers
from orders_app.models import Order
from offers_app.models import OfferDetail


class OrderSerializer(serializers.ModelSerializer):
    customer_user = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days',
                  'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = ['offer_detail_id']

    def validate_offer_detail_id(self, value):
        if not OfferDetail.objects.filter(id=value).exists():
            raise serializers.ValidationError("OfferDetail does not exist.")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        if getattr(user, 'type', None) != 'customer':
            raise serializers.ValidationError("Only customers can create an order.")

        detail_id = validated_data.pop('offer_detail_id')
        detail = OfferDetail.objects.get(id=detail_id)
        offer = detail.offer

        order = Order.objects.create(
            customer_user=user,
            business_user=offer.user,
            offer_detail=detail,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
            status='in_progress'
        )
        return order

    def to_representation(self, instance):
        return OrderSerializer(instance, context=self.context).data


class OrderStatusUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        allowed_status = [choice[0] for choice in Order.STATUS_CHOICES]
        if value not in allowed_status:
            raise serializers.ValidationError(
               f"Invalid status. Allowed values: {allowed_status}"
            )
        return value

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

    def to_representation(self, instance):
        return OrderSerializer(instance, context=self.context).data

