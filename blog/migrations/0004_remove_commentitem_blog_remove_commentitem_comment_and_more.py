# Generated by Django 4.2.6 on 2023-12-03 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blog_short_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentitem',
            name='blog',
        ),
        migrations.RemoveField(
            model_name='commentitem',
            name='comment',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='CommentItem',
        ),
    ]
