# Generated by Django 5.0.2 on 2024-04-30 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='etkinlik',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='etkinlik_images'),
        ),
    ]
