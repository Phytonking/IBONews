from django.urls import path, re_path

import encyclopedia.views as wv

app_name = "encyclopedia"
urlpatterns = [
    path("", wv.index, name="index"),
    path("article/<uuid:articleID>", wv.article_view, name="article"),
    path("search", wv.search_result, name="search"),
    path("about", wv.about, name="about"),
    path("login", wv.login_view, name="login"),
    path("register", wv.register_view, name="register"),
    path("logout", wv.logout_view, name="logout"),
    path("random", wv.random_result, name="random"),
    path("c/<str:classif>", wv.classification_view, name="topic"),
    path("featured", wv.featured_view, name="featured"),
    path("liked", wv.liked_view, name="liked"),
    path("author/<str:AuthorName>", wv.author_page, name="author"),
    path("comment/<uuid:articleID>", wv.comment_view, name="comment"),
    path("comment/<uuid:articleID>/<uuid:commentID>/delete", wv.del_comment, name="del_comment"),
    path("comment/<uuid:articleID>/<uuid:commentID>/edit", wv.edit_comment, name="edit_comment"),
    path("like/<uuid:articleID>", wv.like, name="like"),
    #path("unsubscribe/<str:email>", wv.unsubscriber_view, name="unsubscribe"),
    path("settings", wv.settings, name="settings"),
    path("newsletter", wv.newsletter_management, name="newsletter")
    
]
