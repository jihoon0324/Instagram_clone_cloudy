from django.urls import path

from .views import Profile ,SwitchAccount ,ProfileUpload


app_name="users"
urlpatterns = [

    path('', Profile.as_view() , name="Profile"),
    path('switchAccount', SwitchAccount.as_view() , name="SwitchAccount"),
    path('profile/upload', ProfileUpload.as_view(), name="ProfileUpload")

]