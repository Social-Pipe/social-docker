from rest_framework import serializers
from app.clients.models import Client, Post, PostFile, Comment
from app.payments.serializers import SubscriptionSerializer

class ClientSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(
        max_length=None, allow_empty_file=True, use_url=False)
    subscription = SubscriptionSerializer(many=False)

    class Meta:
        model = Client
        fields = ['id', 'logo', 'name', 'access_hash',
                  'instagram', 'facebook', 'linkedin', 'subscription']


class CreateClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'url', 'logo', 'name', 'password',
                  'instagram', 'facebook', 'linkedin']

class PatchClientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    
    class Meta:
        model = Client
        fields = ['logo', 'name', 'instagram', 'facebook', 'linkedin']

class PostFileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(
        max_length=None, allow_empty_file=True, use_url=False)

    class Meta:
        model = PostFile
        fields = ['id', 'file', 'order', 'created_at']


class CreatePostFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostFile
        fields = ['post', 'file', 'order']


class CreatePostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['caption',
                  'instagram', 'facebook', 'linkedin', 'posting_date', 'publish', 'type', 'status']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'writer', 'message', 'created_at']


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'writer', 'message']


class PostSerializer(serializers.ModelSerializer):
    files = PostFileSerializer(many=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'files', 'caption',
                  'instagram', 'facebook', 'linkedin', 'created_at', 'posting_date', 'publish', 'type', 'status', 'archive', 'comments']
        depth = 2


class ClientObtainTokenSerializer(serializers.Serializer):
    access_hash = serializers.CharField()
    password = serializers.CharField()
