# Generated by Django 4.0.2 on 2022-02-21 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_remove_subscription_blog_author_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='blog_author',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='subscriber',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]
