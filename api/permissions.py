
from rest_framework import permissions


class UserIsOwnerBlogPost(permissions.BasePermission):

    def has_object_permission(self, request, view, blogpost):

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.id == blogpost.user.id
