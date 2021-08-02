from django.urls import path
from .views import AddPost, Home, Login, LogOut
from .utils import check

app_name = 'insta'
urlpatterns = [
    path('home', Home.as_view()),
    path('addpost', AddPost.as_view()),
    path('login', Login.as_view()),
    path('logout', LogOut.as_view()),
    path('check', check)
]
