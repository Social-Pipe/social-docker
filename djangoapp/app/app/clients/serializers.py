from rest_framework import serializers
from app.clients.models import Client


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'url', 'logo', 'name', 'access_hash',
                  'instagram', 'facebook', 'linkedin', 'user']
        depth = 1
