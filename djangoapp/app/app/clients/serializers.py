from rest_framework import serializers
from app.clients.models import Client, Post, PostFile, Comment


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    logo = serializers.ImageField(
        max_length=None, allow_empty_file=True, use_url=False)

    class Meta:
        model = Client
        fields = ['id', 'logo', 'name', 'access_hash',
                  'instagram', 'facebook', 'linkedin']


class CreateClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'url', 'logo', 'name', 'password', 
                  'instagram', 'facebook', 'linkedin']


class PostFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostFile
        fields = ['id', 'file', 'created_at']
        depth = 1


class PostSerializer(serializers.HyperlinkedModelSerializer):
    files = PostFileSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'files', 'caption',
                  'instagram', 'facebook', 'linkedin', 'created_at', 'posting_date', 'publish', 'type', 'status']
        depth = 2


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'writer', 'message', 'created_at']


class ClientObtainTokenSerializer(serializers.Serializer):
    access_hash = serializers.CharField()
    password = serializers.CharField()
