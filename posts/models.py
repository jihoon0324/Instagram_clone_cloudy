from django.db import models
from users.models import User as User_Models
# Create your models here.

class TimeStampedModel(models.Model):
    create_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now_add=True)
    #  이클래스  옵션으로 인해 timeStempedModel 테이블이 만들어 지지 않는다
    class Meta:
        abstract =True


class Post(TimeStampedModel):
    author = models.ForeignKey(User_Models, null=True, on_delete=models.CASCADE , related_name='post_author')
    postContent = models.TextField(blank=False)
    image = models.TextField(blank=False)
    image_likes= models.ManyToManyField(User_Models, related_name="post_image_like" ,blank=True)


class Comment(TimeStampedModel):
    author = models.ForeignKey(User_Models, null=True, on_delete=models.CASCADE, related_name='comment_author')
    posts = models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name="comment_post")
    commentContents = models.TextField(blank=True)