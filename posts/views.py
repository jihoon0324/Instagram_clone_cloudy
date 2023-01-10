import os
from uuid import uuid4
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from Instagram_clone.settings import MEDIA_ROOT
from users.models import User
from . import models, serializers
from django.http import JsonResponse


# Create your views here.

class Main(APIView):

    def get(self, request):
        nickname = request.session.get('nickname')

        if nickname is None:
            request.session['nickname'] = "A_nickname"
        nickname = request.session.get('nickname')
        user = User.objects.filter(nickname=nickname).first()

        following = user.following.all()
        posts = models.Post.objects.filter(
            Q(author__in=following) | Q(author=user)

        ).order_by("-create_at")

        serializer = serializers.PostSerializer(posts, many=True)
        return render(request, "posts/postsMain.html", {"user": user, "posts": serializer.data})


class UploadPost(APIView):

    def post(self, request):
        nickname = request.session.get('nickname')
        user = User.objects.filter(nickname=nickname).first()
        file = request.FILES['file']
        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        image = uuid_name
        content = request.data.get('content')
        models.Post.objects.create(author=user, postContent=content, image=image)
        return Response(status=200)


class PostLike(APIView):

    def post(self, request):
        response_body = {"result": "", "postId": ""}
        nickname = request.session.get('nickname')
        user = User.objects.filter(nickname=nickname).first()
        postId = request.data.get('postId', None)
        post_id = postId.split("_")
        response_body["postId"] = postId
        post = models.Post.objects.filter(pk=post_id[1]).first()
        existed_user = post.image_likes.filter(pk=user.id).exists()

        if existed_user:
            post.image_likes.remove(user.id)
            response_body["result"] = "dislike"
        else:
            post.image_likes.add(user.id)
            response_body["result"] = "like"

        return JsonResponse(status=200, data=response_body)


class CommentCreate(APIView):

    def post(self, request):
        response_body = {"user_nickname": "", "comment_content": ""}
        nickname = request.session.get('nickname')
        user = User.objects.filter(nickname=nickname).first()
        response_body["user"] = user.nickname
        comment_content = request.data.get('comment_content', None)
        response_body["comment_content"] = comment_content
        postId = request.data.get('postId', None)

        post = models.Post.objects.filter(pk=postId).first()

        models.Comment.objects.create(author=user, commentContents=comment_content, posts=post)

        return JsonResponse(status=200, data=response_body)


class CommentDelete(APIView):

    def post(self, request):
        response_body = {"user": "", "comment": ""}
        nickname = request.session.get('nickname')
        user = User.objects.filter(nickname=nickname).first()
        commentId = request.data.get('commentId', None)
        response_body["user"] = user.id
        comment = models.Comment.objects.filter(pk=commentId).first()
        response_body["comment"] = comment
        if user.id == comment.author_id:
            comment.delete()

        return Response(status=200)
