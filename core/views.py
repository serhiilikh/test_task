from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions

from .models import Post, Reaction
from .serializers import UserSerializer, PostSerializer, ReactionSerializer


class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CreatePost(generics.CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class SignUp(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class ReactionView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, is_reaction_like=None):
        if is_reaction_like is not None:
            # this is "like" or "unlike" action
            post = get_object_or_404(Post, pk=pk)
            res = Reaction.create_if_like_else_delete(post=post, create=is_reaction_like, user=request.user)
            return Response({'status': res})

        # this is request to get reactions related to post
        reactions = Reaction.objects.filter(post__id=pk) if pk else Reaction.objects.all()
        serializer = ReactionSerializer(reactions, many=True)
        return Response(serializer.data)

