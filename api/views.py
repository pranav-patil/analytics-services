from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from records.models import BlogPost
from .permissions import UserIsOwnerBlogPost
from .serializers import BlogPostSerializer


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
