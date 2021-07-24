from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    nickname = models.TextField(max_length=15, null=False)
    name = models.TextField(max_length=100, null=False)
    password = models.TextField(max_length=50, null=False)
    salt = models.TextField(max_length=10, null=False)
    is_admin = models.SmallIntegerField(null=False, default=0)
    profile_pic = models.ImageField(upload_to='profile_pic', null=False, default='/profile_pic/default.png')
    introduce = models.TextField(max_length=150, null=False, default="")
