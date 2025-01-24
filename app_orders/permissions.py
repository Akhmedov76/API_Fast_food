from rest_framework.permissions import BasePermission

"""
Permission classes for the food ordering application.
IsWaiter: Only waiters can access this viewset.
"""


class IsWaiter(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'waiter'
