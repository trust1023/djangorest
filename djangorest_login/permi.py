
from rest_framework.permissions import BasePermission


class ViPPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.usertype >= 2:
            return True
        return False