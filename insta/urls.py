from django.urls import path
<<<<<<< HEAD
from .views import AddPost, Home, Login, LogOut, MyPage, PostsView
=======
from .views import AddPost, EditPost, Home, Login, LogOut
>>>>>>> 8d4f8cb9cafb15646c38754f41adf9c4c022bf9a
from .utils import check

app_name = 'insta'
urlpatterns = [
    path('home', PostsView.as_view()),
    path('addpost', AddPost.as_view()),
    path('editpost', EditPost.as_view()),
    path('login', Login.as_view()),
    path('logout', LogOut.as_view()),
    path('check', check),
    path('mypage', MyPage.as_view())
]
