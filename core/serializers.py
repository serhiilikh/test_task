from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer, CharField

from .models import Post, Reaction


class UserSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = User
        required = ("id", "username", "password", 'email')
        fields = ("id", "username", "password", 'email')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_active=True
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        post.save()
        return post


class ReactionSerializer(ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'
