from django.db import models
from BlogApp import settings


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_users', null=True)
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_users',
                             null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    sub_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    text = models.TextField()

    def __str__(self):
        return self.text
