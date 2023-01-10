from rest_framework import serializers
from users.models import User
from . import models

class FeedAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "nickname",
            "profile_image",
            "name"
        )




class CommentSerializer(serializers.ModelSerializer):
    author =FeedAuthorSerializer()
    class Meta:
        model = models.Comment
        fields = (
            "id",
            "commentContents",
            "author",
        )








class PostSerializer(serializers.ModelSerializer):
    comment_post = CommentSerializer(many=True)
    author = FeedAuthorSerializer()

    class Meta:
        model = models.Post
        fields = (
            "id",
            "image",
            "postContent",
            "comment_post",
            "author",
            "image_likes"
        )