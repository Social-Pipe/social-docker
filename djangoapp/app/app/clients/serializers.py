from rest_framework import serializers
from app.clients.models import Client


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    logo = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=False)

    class Meta:
        model = Client
        fields = ['id', 'logo', 'name', 'access_hash',
                  'instagram', 'facebook', 'linkedin']


class CreateClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'url', 'logo', 'name',
                  'instagram', 'facebook', 'linkedin']
