# Generated by Django 2.2 on 2019-12-26 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20191103_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='image/'),
        ),
    ]
