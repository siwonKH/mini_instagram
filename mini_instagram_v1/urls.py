from django.urls import path, include
from insta.views import Home, PostsView
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.views.static import serve


# MEDIA 파일 보호
def protected_file(request, path, document_root=None):
    user_pk = request.session.get('user')
    if user_pk:
        return serve(request, path, document_root)
    return redirect('/')


urlpatterns = [
    path('', include('insta.urls')),
<<<<<<< HEAD
    path('', PostsView.as_view(),  name="posts"),
    # path('', Home.as_view()),
=======
    path('', PostsView.as_view(), name="posts"),
    path('', Home.as_view()),  # this should be gone
>>>>>>> 8d4f8cb9cafb15646c38754f41adf9c4c022bf9a

] + static(settings.MEDIA_URL, protected_file, document_root=settings.MEDIA_ROOT)
