# Generated by Django 4.1.4 on 2023-03-01 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_blog_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]
