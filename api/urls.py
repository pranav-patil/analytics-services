from django.urls import path

from .views import BlogPostListCreateAPIView, BlogPostDetailAPIView, VideoGameSalesView

app_name = 'api'

urlpatterns = [
    path('postings/', BlogPostListCreateAPIView.as_view(), name="list"),
    path('postings/<int:pk>', BlogPostDetailAPIView.as_view(), name="detail"),
    path('videogames/sales/', VideoGameSalesView.as_view(), name="file"),
]
