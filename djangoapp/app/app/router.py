from app.posts.viewsets import PostViewSet
from app.core.views import UserViewSet, GroupViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register('posts', PostViewSet)