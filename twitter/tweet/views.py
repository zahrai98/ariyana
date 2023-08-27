from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from . import models, serializers
# from twitter.account import models as account_models


class PostRetriveCreateDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, format=None, *args, **kwargs):
        post = models.Post.objects.filter(user=request.user, pk=self.kwargs['post_id'])
        serialized_post = serializers.PostSerializer(post)
        return Response(serialized_post.data, status=status.HTTP_200_OK)

    def post(self, request, format=None, *args, **kwargs):
        """
        Create a new post 
        """
        data = request.data.copy()
        data['user'] = request.user
        serialized_post = serializers.PostSerializer(data=data)
        serialized_post.is_valid(raise_exception=True)
        models.Post.objects.create(**serialized_post.validated_data)
        return Response(serialized_post.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, format=None, *args, **kwargs):
        """
        Delete a post 
        """
        post = models.Post.objects.filter(user=request.user, pk=self.kwargs['post_id'])
        if post.exists():
           post.delete()
           return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, format=None, *args, **kwargs):
        data = request.data
        data['user'] = request.user
        post = get_object_or_404(models.Post, pk=self.kwargs['post_id'])
        serialized_post = serializers.PostSerializer(post, data)
        if serialized_post.is_valid():
            serialized_post.save()
            return Response(serialized_post.data)
        return Response(serialized_post.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, format=None):
        posts = request.user.posts.all()
        serialized_posts = serializers.PostSerializer(posts, many=True)
        return Response(serialized_posts.data, status=status.HTTP_200_OK)
    

class FollowingPostListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, format=None):
        # posts = User.objects.filter(followers=request.user).prefetch_related('posts')
        posts = models.Post.objects.filter(user_followers=request.user)
        serialized_posts = serializers.PostSerializer(posts, many=True)
        return Response(serialized_posts.data, status=status.HTTP_200_OK)