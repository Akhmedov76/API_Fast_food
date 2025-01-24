from rest_framework.permissions import BasePermission

"""
Permission classes for the food ordering application.
IsAdmin: Only staff users can access this viewset.
IsUser: Only authenticated users can access this viewset.
"""


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'user'
