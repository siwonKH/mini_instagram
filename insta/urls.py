from django.urls import path
from .views import Home, UserDetailView, PostPage, AddPost, Comment, EditPost, DeletePost, EmailVerify, ResendEmail, SignUp, Login, LogOut, MyPage, SettingPage, ChangePwPage, FindingPwPage, AddHeart, CheckHeart
from .utils import check
from ratelimit.decorators import ratelimit

app_name = 'insta'
urlpatterns = [
    path('home', Home.as_view()),
    path('@<str:nickname>', UserDetailView.as_view(), name='user_detail'),
    path('post', PostPage.as_view()),
    path('addpost', AddPost.as_view()),
    path('editpost', EditPost.as_view()),
    path('deletepost', DeletePost.as_view()),
    path('verify', EmailVerify.as_view()),
    path('resendemail', ResendEmail.as_view()),
    path('comment', Comment.as_view()),
    path('signup', SignUp.as_view()),
    path('login', Login.as_view()),
    path('logout', LogOut.as_view()),
    path('check', check),
    path('mypage', MyPage.as_view()),
    path('setting', SettingPage.as_view()),
    path('changepw', ChangePwPage.as_view()),
    path('findpw', FindingPwPage.as_view()),
    path('addheart', AddHeart.as_view()),
    path('checkheart', CheckHeart.as_view()),
]
