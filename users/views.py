from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from Instagram_clone.settings import MEDIA_ROOT
import os
from django.db.models import Q
from posts import models ,serializers
from uuid import uuid4

from .models import User
# Create your views here.

class Profile(APIView):

    def get(self, request):
        nickname = request.session.get('nickname')
        user = User.objects.filter(nickname=nickname).first()
        following = user.following.all()
        posts = models.Post.objects.filter(
            Q(author__in=following) | Q(author=user)

        ).order_by("-create_at")

        serializer = serializers.PostSerializer(posts, many=True)
        return render(request, "users/profile.html",{ "user": user ,"posts":serializer.data  })
        # return Response({ "user": user ,"posts":serializer.data  },status=200 )

class SwitchAccount(APIView):
    def post(self, request):

        nickname = request.data.get('nickname' ,None )

        request.session.flush()
        request.session['nickname'] = nickname

        return Response(status=200)

class ProfileUpload(APIView):

    def post(self,request):
        file = request.FILES['file']
        nickname = request.session.get('nickname')
        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        profile_image = uuid_name
        user = User.objects.filter(nickname=nickname).first()
        user.profile_image = profile_image
        user.save()

        return Response(status=200)