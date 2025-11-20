from rest_framework import serializers
from orders_app.models import Order
from offers_app.models import OfferDetail

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.

    Converts Order instances to JSON and vice versa for API responses.
    Includes read-only references to customer and business users.
    """
    customer_user = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days',
                  'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new Order from an existing OfferDetail.

    Handles:
    - Validating that the specified OfferDetail exists
    - Creating the Order with data copied from the OfferDetail
    - Setting customer_user and business_user automatically
    """
    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = ['offer_detail_id']

    def validate_offer_detail_id(self, value):
        """
        Ensure the provided OfferDetail ID exists.

        Raises:
            serializers.ValidationError: If OfferDetail does not exist
        """
        if not OfferDetail.objects.filter(id=value).exists():
            raise serializers.ValidationError("OfferDetail does not exist.")
        return value

    def create(self, validated_data):
        """
        Create a new Order instance based on the selected OfferDetail.

        Steps:
        1. Retrieve the authenticated user from the request.
        2. Get the OfferDetail instance using the provided ID.
        3. Copy relevant fields from OfferDetail to the new Order.
        4. Set customer_user and business_user automatically.
        5. Set initial status to 'in_progress'.
        """
        request = self.context.get('request')
        user = request.user

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
        """
        Use the standard OrderSerializer for the response representation.
        """
        return OrderSerializer(instance, context=self.context).data


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating the status of an Order.

    Handles:
    - Validating that the new status is one of the allowed choices
    - Updating the status field of the Order
    - Returning a serialized representation of the updated Order
    """
    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        """
        Ensure that the provided status is one of the allowed choices.

        Raises:
            serializers.ValidationError: If the status is invalid
        """
        allowed_status = [choice[0] for choice in Order.STATUS_CHOICES]
        if value not in allowed_status:
            raise serializers.ValidationError(
               f"Invalid status. Allowed values: {allowed_status}"
            )
        return value

    def update(self, instance, validated_data):
        """
        Update the status of the Order instance.

        Args:
            instance: The Order instance to update
            validated_data: Validated data containing the new status

        Returns:
            The updated Order instance
        """
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Use the standard OrderSerializer for the response representation.
        """
        return OrderSerializer(instance, context=self.context).data

