# Generated by Django 3.1.4 on 2020-12-16 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0005_auto_20201216_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='global_score',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Note globale'),
        ),
    ]