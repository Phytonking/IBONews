# Generated by Django 4.2.3 on 2023-08-17 01:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_id', models.UUIDField()),
                ('title', models.TextField()),
                ('author', models.TextField()),
                ('date_published', models.DateTimeField()),
                ('textual_content', models.TextField()),
                ('description', models.TextField(null=True)),
                ('featured', models.BooleanField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('first_name', models.TextField(null=True)),
                ('last_name', models.TextField(null=True)),
                ('username', models.TextField(null=True)),
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('password', models.TextField(null=True)),
                ('is_subscribed', models.BigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='LikedArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='articleTheUserLiked', to='encyclopedia.article')),
                ('liker', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='userWhoLikedTheArticle', to='encyclopedia.user')),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('bio', models.TextField()),
                ('location', models.TextField()),
                ('online_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='authorUser', to='encyclopedia.user')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_commented', models.DateTimeField(auto_created=True, null=True)),
                ('comment_content', models.TextField(null=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='articleTheUserCommentedOn', to='encyclopedia.article')),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='commenter', to='encyclopedia.user')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='article_classification',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='classificationOfArticle', to='encyclopedia.classification'),
        ),
    ]
