from app.core.viewsets import UserViewSet, GroupViewSet
from app.clients.viewsets import ClientViewSet, PostViewSet, PostFileViewSet, CommentViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'posts', PostViewSet)
router.register(r'postfiles', PostFileViewSet)
router.register(r'comments', CommentViewSet)
