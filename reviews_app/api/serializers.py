from rest_framework import serializers
from auth_app.models import CustomUser
from reviews_app.models import Review
from django.utils import timezone


class ReviewSerializer(serializers.ModelSerializer):

    business_user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all())
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

    business_user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(type="business"))

    class Meta:
        model = Review
        fields = ["business_user", "rating", "description"]

    def validate(self, attrs):
        request = self.context["request"]
        reviewer = request.user
        business_user = attrs["business_user"]

        if reviewer.type != "customer":
            raise serializers.ValidationError(
                "Only customers can create reviews.")

        if business_user.type != "business":
            raise serializers.ValidationError(
                "You can only review business users.")

        if Review.objects.filter(business_user=business_user, reviewer=reviewer).exists():
            raise serializers.ValidationError(
                "You have already reviewed this business user.")

        return attrs

    def create(self, validated_data):
        reviewer = self.context["request"].user
        review = Review.objects.create(
            reviewer=reviewer,
            **validated_data
        )
        return review


class ReviewUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['rating', 'description']
    
    def validate(self, attrs):

        if 'rating' not in attrs or 'description' not in attrs:
            raise serializers.ValidationError(
                "'raiting and description are required"
            )
        
        return attrs

    def update(self, instance, validated_data):
        if not validated_data:
            raise serializers.ValidationError("No data provided for update.")
        
    

        instance.rating = validated_data.get('rating', instance.rating)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.save()
        return instance

    def to_representation(self, instance):
        return ReviewSerializer(instance, context=self.context).data
