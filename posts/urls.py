from django.urls import path

from .views import Main, UploadPost, PostLike ,CommentCreate ,CommentDelete

app_name = "posts"
urlpatterns = [

    path('', Main.as_view(), name="Main"),
    path('upload', UploadPost.as_view()),
    path('postLike', PostLike.as_view()),
    path('commentCreate', CommentCreate.as_view()),
    path('commentDelete', CommentDelete.as_view()),
]
