from django.urls import path, include
from insta.views import Home, PostsView
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect


# MEDIA 파일 보호
def protected_file(request, path, document_root=None):
    return redirect('/')


urlpatterns = [
    path('', include('insta.urls')),
    path('', PostsView.as_view(), name="posts"),
    path('', Home.as_view()),

] + static(settings.MEDIA_URL, protected_file, document_root=settings.MEDIA_ROOT)
