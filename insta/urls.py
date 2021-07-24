from django.urls import path
from .views import Home, Login, LogOut

app_name = 'insta'
urlpatterns = [
    path('home', Home.as_view()),
    path('login', Login.as_view()),
    path('logout', LogOut.as_view()),
]
