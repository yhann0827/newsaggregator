from datetime import timezone
from rest_framework import serializers
from .models import NewsStory


class NewsStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsStory
        fields = ['headline', 'story_cat', 'story_region', 'details', 'author']
        extra_kwargs = {
            'author': {'read_only': True},  # Set author field as read-only
            'story_date': {'read_only': True},    # Set date field as read-only
        }

    def create(self, validated_data):
        # Automatically set author field to the current user
        validated_data['author'] = self.context['request'].user
        # Automatically set date field to the current timestamp
        validated_data['date'] = timezone.now()
        return super().create(validated_data)