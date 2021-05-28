from app.core.viewsets import UserViewSet, GroupViewSet
from app.clients.viewsets import ClientViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'clients', ClientViewSet)