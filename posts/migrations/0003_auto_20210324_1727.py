# Generated by Django 3.1.7 on 2021-03-25 00:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20210324_1633'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postlike',
            old_name='tweet',
            new_name='post',
        ),
    ]
