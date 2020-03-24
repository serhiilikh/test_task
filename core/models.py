from django.db import models

from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=1000, blank=False)
    text = models.TextField(blank=False)


class Reaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def create_if_like_else_delete(cls, post, create, user):
        inst = cls.objects.filter(post=post, user=user).first()
        if inst:
            if create:
                return 'already created'
            inst.delete()
            return 'deleted'
        if create:
            cls.objects.get_or_create(post=post, user=user)
            return 'created'
        return 'already unliked or not liked'
