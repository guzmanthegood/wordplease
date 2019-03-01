from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from django.contrib.auth.models import User
from blogs.models import Post

from . import serializers
from .permissions import UserPermission, PostPermission

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (UserPermission,)
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        return serializers.UserListSerializer if self.action == 'list' else serializers.UserSerializer


class BlogViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = serializers.BlogSerializer

    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['username', 'first_name', 'last_name']
    filter_fields = ['username', 'first_name', 'last_name']
    ordering_fields = ['username', 'first_name', 'last_name']
    ordering = ['username']

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (PostPermission,)
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['title', 'description']
    filter_fields = ['title', 'description']
    ordering = ['-pub_date']
    ordering_fields = ['pub_date', 'owner__username']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PostList(generics.ListAPIView):    
    serializer_class = serializers.PostListSerializer
    permission_classes = (AllowAny,)
    lookup_url_kwarg = "username"

    def get_queryset(self):
        username = self.kwargs.get(self.lookup_url_kwarg)
        posts = Post.objects.filter(owner__username=username)
        return posts