# Generated by Django 3.2.5 on 2021-07-14 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0005_auto_20210713_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='post',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='feed.post'),
        ),
    ]
