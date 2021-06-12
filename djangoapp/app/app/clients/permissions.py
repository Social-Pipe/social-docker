from rest_framework import permissions
from django.conf import settings
from pprint import pprint
from app.clients.models import Client
import jwt
from pprint import pprint


class IsAuthenticatedOrIsClient(permissions.BasePermission):
    """
    Check if user is authenticated or has client JWT long
    access Token
    """

    def has_permission(self, request, view):
        print('================== PERMISSION ===================')
        # Recognize user login
        loggedin_id = request.user.id
        
        if loggedin_id:
            # Check if logged in user is an admin
            is_admin = request.user.is_admin
            if is_admin:
                return True
        
        if 'X-Client' in request.headers:
            jwt_token = request.headers['X-Client'][7:]
            decoded_jwt = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
            if decoded_jwt['scope'] == 'client':
                client = Client.objects.get(id=2)
                request._client = client
            pprint(request.__dict__)
            return True

        if loggedin_id:
            return True

        return False
