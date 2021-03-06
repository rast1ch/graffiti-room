# Generated by Django 3.2.5 on 2021-07-13 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0004_alter_post_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='image',
            name='img',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, max_length=6, unique=True),
        ),
    ]
