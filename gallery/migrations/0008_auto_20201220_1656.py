# Generated by Django 3.1.4 on 2020-12-20 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0007_auto_20201218_1706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='comment_visual',
        ),
        migrations.RemoveField(
            model_name='review',
            name='score_visual',
        ),
    ]
