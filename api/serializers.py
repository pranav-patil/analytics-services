from rest_framework import serializers
from records.models import BlogPost
from .models import VideoGameSales, SuicideStatistics
from rest_pandas import PandasSerializer


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


class SuicideStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuicideStatistics
        exclude = ['id']
