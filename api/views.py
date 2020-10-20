from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from records.models import BlogPost
from .permissions import UserIsOwnerBlogPost
from .serializers import BlogPostSerializer
from rest_pandas import PandasSimpleView, PandasJSONRenderer
import pandas as pd


class BlogPostListCreateAPIView(ListCreateAPIView):
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        return BlogPost.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BlogPostDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()
    permission_classes = (IsAuthenticated, UserIsOwnerBlogPost)


# class BlogPostRudView(RetrieveUpdateDestroyAPIView):
#     lookup_field = 'pk'  # slug, id
#     queryset = BlogPost.objects.all()
#
#     def get_queryset(self):
#         return BlogPost.objects.all()
#
#     def get_object(self):
#         pk = self.kwargs.get("pk")
#         return BlogPost.objects.get(pk=pk)


class VideoGameSalesView(PandasSimpleView):
    renderer_classes = [PandasJSONRenderer]

    def get_data(self, request, *args, **kwargs):
        return pd.read_csv('data/vgsales.csv')

    def transform_dataframe(self, dataframe):
        dataframe.some_pivot_function(in_place=True)
        return dataframe
