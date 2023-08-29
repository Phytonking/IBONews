from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Subscriber(models.Model):
    subscriber_person = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="subscriber")
    is_subscribed = models.BooleanField(null=True)

class Classification(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.TextField()
    bio = models.TextField()
    location = models.TextField()
    online_user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="authorUser", null=True
    )

# Create your models here.
class Article(models.Model):
    article_id = models.UUIDField()
    title = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING, related_name="creator", null=True)
    date_published = models.DateTimeField()
    image = models.URLField(null=True)
    textual_content = models.TextField()
    description = models.TextField(null=True)
    article_classification = models.ForeignKey(
        Classification,
        on_delete=models.DO_NOTHING,
        related_name="classificationOfArticle",
        null=True,
    )
    featured = models.BooleanField(null=True)

    def __str__(self):
        return str(self.article_id)


class LikedArticle(models.Model):
    liker = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="userWhoLikedTheArticle"
    )
    article = models.ForeignKey(
        Article, on_delete=models.DO_NOTHING, related_name="articleTheUserLiked"
    )


class ArticleComment(models.Model):
    commentid = models.UUIDField(null=True)
    commenter = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="commenter"
    )
    article = models.ForeignKey(
        Article, on_delete=models.DO_NOTHING, related_name="articleTheUserCommentedOn"
    )
    date_commented = models.DateTimeField(auto_created=True, null=True)
    comment_content = models.TextField(null=True)

    def __str__(self):
        return self.commentid
