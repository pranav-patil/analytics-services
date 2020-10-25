from rest_framework import serializers
from records.models import BlogPost
from .models import VideoGameSales


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = [
            'pk',
            'user',
            'title',
            'content',
            'timestamp',
        ]


class VideoGameSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoGameSales
        fields = '__all__'
