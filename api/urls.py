from django.urls import path

from .views import BlogPostListCreateAPIView, BlogPostDetailAPIView, VideoGameSalesView, SuicideStatisticsView

app_name = 'api'

urlpatterns = [
    path('postings/', BlogPostListCreateAPIView.as_view(), name="postings"),
    path('postings/<int:pk>', BlogPostDetailAPIView.as_view(), name="posting_detail"),
    path('videogames/sales/', VideoGameSalesView.as_view(), name="video_games_sales"),
    path('videogames/sales/chart/', VideoGameSalesView.as_view(), {'chart': True}, name="video_games_sales_chart"),
    path('suicide/statistics/', SuicideStatisticsView.as_view(), name="suicide_statistics")
]
