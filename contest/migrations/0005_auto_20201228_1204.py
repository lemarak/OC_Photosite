# Generated by Django 3.1.4 on 2020-12-28 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0004_auto_20201228_1007'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contestpicture',
            old_name='id_contest',
            new_name='contest',
        ),
        migrations.RenameField(
            model_name='contestpicture',
            old_name='id_picture',
            new_name='picture',
        ),
        migrations.RenameField(
            model_name='vote',
            old_name='id_contest_picture',
            new_name='contest_picture',
        ),
        migrations.RenameField(
            model_name='vote',
            old_name='id_user',
            new_name='user',
        ),
    ]
