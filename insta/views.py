import hashlib
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import views
from django.contrib.auth import logout
from .models import User, Post
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required


class PostsView(ListView):
    model = Post
    paginate_by = 1
    context_object_name = 'posts'
    template_name = 'index.html'
    ordering = ['id']


def check(request):
    user_pk = request.session.get('user')
    if user_pk:
        context = {'s': 'true'}
        return HttpResponse(json.dumps(context), content_type="application/json")
    context = {'s': 'false'}
    return HttpResponse(json.dumps(context), content_type="application/json")


class Home(views.View):
    @staticmethod
    def post(request):
        return redirect('/')

    @staticmethod
    def get(request):
        user_pk = request.session.get('user')  # 요청을 보낸 사용자의 세션 확인
        if user_pk:  # 세션이 비어있지 않다면
            return redirect('/')

        return redirect('/login')


# noinspection PyBroadException
class AddPost(views.View):
    @staticmethod
    def post(request):
        user_pk = request.session.get('user')
        if user_pk:
            user = User.objects.get(id=user_pk)
        else:
            return redirect('/login')

        # 폼에서 받은 정보 가져오기
        description = request.POST['desc']
        try:
            image = request.FILES['img']
        except:
            return redirect('/addpost')

        post = Post()
        post.author = user
        if description:
            post.description = description
        post.image = image
        post.save()

        return redirect('/')

    @staticmethod
    def get(request):
        user_pk = request.session.get('user')
        if user_pk:
            return render(request, 'add_post.html')
        return redirect('/login')


class EditPost(views.View):
    @staticmethod
    def post(request):
        try:
            post_id = request.POST['id']
            post = Post.objects.get(id=post_id)  # 게시글 테이블에서 정보 가져오기
        except:
            return redirect('/')

        user_pk = request.session.get('user')
        if not user_pk:
            return redirect('/login')

        if str(user_pk) != str(post.author.id):  # 수정하려는 사람과 작성자가 다르다면
            return redirect('/')

        description = request.POST['desc']
        try:
            image = request.FILES['img']
            post.image.delete()
            post.save()
            post.image = image
        except:
            pass

        post.description = description
        post.save()
        return redirect('/')

    @staticmethod
    def get(request):
        user_pk = request.session.get('user')
        if not user_pk:
            return redirect('/login')

        try:
            post_id = request.GET['id']
            post = Post.objects.get(id=post_id)  # 게시글 테이블에서 정보 가져오기
        except:
            return redirect('/')

        if str(user_pk) != str(post.author.id):  # 수정하려는 사람과 작성자가 다르다면
            return redirect('/')

        context = {
            'image': post.image,
            'desc': post.description
        }
        return render(request, 'edit_post.html', context)


class Login(views.View):
    @staticmethod
    def post(request):
        try:
            email = request.POST['email']
            password = request.POST['password']
        except:
            return redirect('/login')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)  # 데이터베이스에서 user_id 에 해당하는 데이터 가져오기
            salted_password = str(user.salt) + str(password)  # 불러온 해당유저 데이터에서, 솔트값을 사용자 입력 값과 합침
            hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()  # 솔트값과 합쳐진 사용자 입력값을 해시

            if str(user.password) == str(hashed_password):
                request.session['user'] = user.id  # 로그인 성공!
                context = {'msg': "success"}
                return HttpResponse(json.dumps(context), content_type="application/json")

            else:
                context = {'msg': "pw_fail"}  # 에러메시지 생성
                return HttpResponse(json.dumps(context), content_type="application/json")
        else:
            context = {'msg': "id_fail"}  # 에러메시지 생성
            return HttpResponse(json.dumps(context), content_type="application/json")

    @staticmethod
    def get(request):
        user_pk = request.session.get('user')  # 사용자 세션 확인
        if user_pk:  # 세션이 비지 않았다면?
            # 여기 왜 왔어~ 로그인 했으면 홈으로 돌아가~
            return redirect('/')

        # 로그인 하세요~
        return render(request, 'sign_in.html')  # 사용자에게 로그인 페이지 보여줌


class LogOut(views.View):
    def post(self, request):
        pass

    # 로그아웃
    @staticmethod
    def get(request):
        logout(request)
        return redirect('/')
