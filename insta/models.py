import os
from django.db import models
from django.conf import settings
from django.utils import timezone
from .validators import validate_file_size
from django.core.validators import validate_image_file_extension


class User(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    email = models.EmailField(max_length=100, null=False, default="example@example.com")
    nickname = models.TextField(max_length=15, null=False)
    name = models.TextField(max_length=100, null=False)
    password = models.TextField(max_length=50, null=False)
    salt = models.TextField(max_length=10, null=False)
    is_admin = models.SmallIntegerField(null=False, default=0)
    profile_pic = models.ImageField(upload_to='profile_pic', null=False, default='/profile_pic/default.png', validators=[validate_file_size, validate_image_file_extension])
    introduce = models.TextField(max_length=50, null=False, default='')
    is_verified = models.BooleanField(default=False)


class Post(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    author = models.ForeignKey(to=User, related_name='post_user', on_delete=models.CASCADE, db_column='post_user')
    image = models.ImageField(upload_to='post_pic', null=False, default=None, validators=[validate_file_size, validate_image_file_extension])
    description = models.TextField(max_length=100, null=False, default='')
    created_at = models.DateTimeField(default=timezone.now)

    def delete(self, *args, **kwargs):  # 게시글을 삭제할때 미디어 파일도 삭제되도록 delete 함수 중간에 가로챔
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
        super(Post, self).delete(*args, **kwargs)


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


class UserFollows(models.Model):
    id = models.AutoField(primary_key=True)
    follower_user = models.ForeignKey(to=User, related_name='follower', on_delete=models.CASCADE, db_column='follower_user')
    following_user = models.ForeignKey(to=User, related_name='following', on_delete=models.CASCADE, db_column='following_user')
