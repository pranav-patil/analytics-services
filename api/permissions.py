from rest_framework.permissions import BasePermission


class UserIsOwnerBlogPost(BasePermission):

    def has_object_permission(self, request, view, blogpost):
        return request.user.id == blogpost.user.id
