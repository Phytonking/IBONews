# Generated by Django 4.2.3 on 2023-08-24 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encyclopedia', '0006_alter_article_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlecomment',
            name='commentid',
            field=models.UUIDField(null=True),
        ),
    ]
