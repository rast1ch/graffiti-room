# Generated by Django 3.2.5 on 2021-08-27 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210716_0302'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='uuid',
            field=models.UUIDField(null=True, unique=True),
        ),
    ]
