from rest_framework import serializers
from auth_app.models import CustomUser
from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.

    Fields:
        - business_user: The business user being reviewed (selectable via PK)
        - reviewer: The user who created the review (read-only, set automatically)
        - rating: Numeric rating for the business
        - description: Text description of the review
        - created_at: Timestamp when the review was created (read-only)
        - updated_at: Timestamp when the review was last updated (read-only)
    """
    business_user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at"
        ]

class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a Review.

    - Only allows selecting business users as the review target.
    - Ensures a reviewer cannot review the same business user multiple times.
    - Returns full ReviewSerializer representation after creation.
    """
    business_user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(type="business"))

    class Meta:
        model = Review
        fields = ["business_user", "rating", "description"]

    def validate(self, attrs):
        """
        Custom validation to ensure that the reviewer has not already
        submitted a review for the same business user.
        """
        reviewer = self.context["request"].user
        business_user = attrs["business_user"]

        if Review.objects.filter(business_user=business_user, reviewer=reviewer).exists():
            raise serializers.ValidationError(
                "You have already reviewed this business user.")

        return attrs

    def create(self, validated_data):
        """
        Create a new Review instance and assign the current user as reviewer.
        """
        reviewer = self.context["request"].user
        review = Review.objects.create(
            reviewer=reviewer,
            **validated_data
        )
        return review
    
    def to_representation(self, instance):
        """
        Use full ReviewSerializer to represent the newly created instance.
        """
        return ReviewSerializer(instance, context=self.context).data

class ReviewUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating an existing Review.

    Allows updating the 'rating' and 'description' fields only.
    Returns the full ReviewSerializer representation after update.
    """
    
    rating = serializers.IntegerField(required=False, min_value=1, max_value=5)
    description = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Review
        fields = ['rating', 'description']
    
    def validate(self, attrs):
        """
        Ensure that both 'rating' and 'description' are provided.
        """

        if 'rating' not in attrs or 'description' not in attrs:
            raise serializers.ValidationError(
                "'raiting and description are required"
            )
        
        return attrs

    def update(self, instance, validated_data):
        """
        Update the Review instance with new rating and description.
        """
      
        instance.rating = validated_data.get('rating', instance.rating)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Represent the updated instance using the full ReviewSerializer.
        """
        return ReviewSerializer(instance, context=self.context).data
