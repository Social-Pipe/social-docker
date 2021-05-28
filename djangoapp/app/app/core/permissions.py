from rest_framework import permissions
from pprint import pprint


class IsAdminOrIsSelf(permissions.BasePermission):
    """
    Just self user or `is_admin` can access
    """

    def has_permission(self, request, view):
        request_id = request.parser_context.get('kwargs', {}).get('pk', None)
        loggedin_id = request.user.id
        is_admin = request.user.is_admin

        if(loggedin_id == int(request_id)):
            return True
        elif is_admin:
            return True
        return False
