from rest_framework import serializers
from django.contrib.auth.models import User
from blogs.models import Post


class UserListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'first_name', 'last_name', 'email')

class UserSerializer(UserListSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'password', 'first_name', 'last_name', 'email')
    
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class BlogSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    api_url = serializers.SerializerMethodField()
    num_posts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'num_posts', 'url', 'api_url')

    def get_url(self, user):
        link = "{}://{}{}{}/".format(self.context['request'].scheme, self.context['request'].get_host(), "/blogs/", user.username)
        return link

    def get_api_url(self, user):
        link = "{}://{}{}{}/".format(self.context['request'].scheme, self.context['request'].get_host(), "/api/v1/blogs/", user.username)
        return link
    
    def get_num_posts(self, user):
        return Post.objects.filter(owner=user).count()


class PostListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'owner', 'title', 'description', 'pub_date', 'image', 'url')

class PostSerializer(PostListSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'owner', 'title', 'description', 'content', 'pub_date', 'image', 'url')

    def get_owner(self, post):
        return post.owner.username