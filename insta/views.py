import hashlib
<<<<<<< HEAD
=======
import json

from django.http import HttpResponse
>>>>>>> 8d4f8cb9cafb15646c38754f41adf9c4c022bf9a
from django.http.response import HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django import views
from django.contrib.auth import logout
from .models import User, Post
from django.views.generic.list import ListView


class PostsView(ListView):
    model = Post
    paginate_by = 1
    context_object_name = 'posts'
    template_name = 'index.html'
    ordering = ['id']


class Home(views.View):
    @staticmethod
    def post(request):
        return HttpResponseNotAllowed('get')

    @staticmethod
    def get(request):
        user_pk = request.session.get('user')  # 요청을 보낸 사용자의 세션 확인
        if user_pk:  # 세션이 비어있지 않다면
<<<<<<< HEAD
            user = User.objects.get(id=user_pk)  # (세션에 있는 아이디 값)에 해당하는 데이터를 데이터 베이스에서 불러옴
            data = {'login': "로그아웃", 'nick': str(user.nickname)}
            return render(request, 'index.html', data)
=======
            return redirect('/')

>>>>>>> 8d4f8cb9cafb15646c38754f41adf9c4c022bf9a
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
<<<<<<< HEAD
        email = request.POST['email']
        password = request.POST['password']
=======
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
>>>>>>> 8d4f8cb9cafb15646c38754f41adf9c4c022bf9a
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)  # 데이터베이스에서 user_id 에 해당하는 데이터 가져오기
            salted_password = str(user.salt) + str(password)  # 불러온 해당유저 데이터에서, 솔트값을 사용자 입력 값과 합침
            hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()  # 솔트값과 합쳐진 사용자 입력값을 해시
<<<<<<< HEAD
            request.session['user'] = user.id
            if str(user.password) == str(hashed_password):  # 비번 화긴
                request.session['user'] = user.id  # 세션에 유저 아이디 저장
                return redirect('/')  # 홈(index.html)으로 리다이렉트
            else:
                data = {'error': "아이디 또는 비밀번호가 다릅니다"}  # 에러메시지 생성
                return render(request, 'sign_in.html', data)  # 에러메시지를 포함하여 sign_in.html 을 사용자에게 보여줌
=======

            if str(user.password) == str(hashed_password):
                request.session['user'] = user.id  # 로그인 성공!
                context = {'msg': "success"}
                return HttpResponse(json.dumps(context), content_type="application/json")
>>>>>>> 8d4f8cb9cafb15646c38754f41adf9c4c022bf9a

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


class MyPage(views.View):
    @staticmethod
    def get(request):
        user_pk = request.session.get('user')
        if user_pk:
            return render(request, 'mypage.html')
        return redirect('/login')
