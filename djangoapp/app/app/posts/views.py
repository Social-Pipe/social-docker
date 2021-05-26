from django.http import HttpResponse, JsonResponse

from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from app.posts.models import Post
from app.posts.serializers import PostSerializer
