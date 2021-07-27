from django.urls import path, include
from insta.views import Home, PostsView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('insta.urls')),
    path('', PostsView.as_view(),  name="posts"),
    path('', Home.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
