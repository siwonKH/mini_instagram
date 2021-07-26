from enum import unique
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone


class User(models.Model):
    id = models.AutoField(primary_key=True)
    nickname = models.TextField(max_length=15, null=False)
    name = models.TextField(max_length=100, null=False)
    password = models.TextField(max_length=50, null=False)
    salt = models.TextField(max_length=10, null=False)
    is_admin = models.SmallIntegerField(null=False, default=0)
    profile_pic = models.ImageField(upload_to='profile_pic', null=False, default='/profile_pic/default.png')
    introduce = models.TextField(max_length=150, null=False, default='')


class Post(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    image = models.ImageField(upload_to='post_pic', null=True, default=None)
    description = models.TextField(max_length=100, null=False, default='')
    created_at = models.DateTimeField(default=timezone.now)


class PostComment(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(to=Post, related_name='post_comment', on_delete=models.CASCADE, db_column='post_id')
    user_id = models.ForeignKey(to=User, related_name='user_comment', on_delete=models.CASCADE, db_column='user_id')
    comment = models.TextField(max_length=100, null=False, default='')
    created_at = models.DateTimeField(default=timezone.now)


class PostLike(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(to=Post, related_name='post_like', on_delete=models.CASCADE, db_column='post_id')
    user_id = models.ForeignKey(to=User, related_name='user_like', on_delete=models.CASCADE, db_column='user_id')