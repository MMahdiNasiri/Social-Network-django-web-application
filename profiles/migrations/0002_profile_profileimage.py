# Generated by Django 3.1.7 on 2021-04-17 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profileImage',
            field=models.ImageField(default='default-profile.jpg', upload_to='profile_pics'),
        ),
    ]
