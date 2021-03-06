# Generated by Django 3.2.5 on 2021-07-27 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postcomment',
            name='post_id',
        ),
        migrations.RemoveField(
            model_name='postcomment',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='postlike',
            name='post_id',
        ),
        migrations.RemoveField(
            model_name='postlike',
            name='user_id',
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default='example@example.com', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='PostComment',
        ),
        migrations.DeleteModel(
            name='PostLike',
        ),
    ]
