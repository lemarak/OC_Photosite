# Generated by Django 3.1.4 on 2020-12-16 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_auto_20201212_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='contest_image',
            field=models.ImageField(default='#', upload_to='', verbose_name='Image du concours'),
        ),
    ]