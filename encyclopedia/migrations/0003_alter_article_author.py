# Generated by Django 4.2.3 on 2023-08-22 03:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('encyclopedia', '0002_subscriber_alter_articlecomment_commenter_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='creator', to='encyclopedia.author'),
        ),
    ]
