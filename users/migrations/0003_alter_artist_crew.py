# Generated by Django 3.2.5 on 2021-07-13 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210713_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='crew',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='artists', to='users.crew'),
        ),
    ]