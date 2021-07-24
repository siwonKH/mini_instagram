import hashlib
from django.shortcuts import render, redirect
from django import views
from django.contrib.auth import logout
from .models import User


class Home(views.View):
    def post(self, request):
        pass

    @staticmethod
    def get(request):
        user_pk = request.session.get('user')  # 요청을 보낸 사용자의 세션 확인
        if user_pk:  # 세션이 비어있지 않다면
            user = User.objects.get(id=user_pk)  # (세션에 있는 아이디 값)에 해당하는 데이터를 데이터 베이스에서 불러옴
            data = {'login': "로그아웃", 'nick': str(user.nickname)}
            return render(request, 'index.html', data)

        data = {'login': "로그인", 'nick': "먼저 로그인 해주세요"}
        return render(request, 'index.html', data)


class Login(views.View):
    @staticmethod
    def post(request):
        user_id = request.POST['user_id']
        password = request.POST['password']

        if User.objects.filter(id=user_id).exists():
            user = User.objects.get(id=user_id)  # 데이터베이스에서 user_id 에 해당하는 데이터 가져오기
            salted_password = str(user.salt) + str(password)  # 불러온 해당유저 데이터에서, 솔트값을 사용자 입력 값과 합침
            hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()  # 솔트값과 합쳐진 사용자 입력값을 해시

            if str(user.password) == str(hashed_password):  # 비번 화긴
                request.session['user'] = user.id  # 세션에 유저 아이디 저장
                return redirect('/home')  # 홈(index.html)으로 리다이렉트
            else:
                data = {'error': "아이디 또는 비밀번호가 다릅니다"}  # 에러메시지 생성
                return render(request, 'sign_in.html', data)  # 에러메시지를 포함하여 sign_in.html 을 사용자에게 보여줌

        else:
            data = {'error': "아이디 또는 비밀번호가 다릅니다", 'user': user_id}
            return render(request, 'sign_in.html', data)

    @staticmethod
    def get(request):
        user_pk = request.session.get('user')  # 사용자 세션 확인

        if user_pk:  # 세션이 비지 않았다면?
            # 여기 왜 왔어~ 로그인 했으면 홈으로 돌아가~
            return redirect('/home')

        # 로그인 하세요~
        return render(request, 'sign_in.html')  # 사용자에게 로그인 페이지 보여줌


class LogOut(views.View):
    def post(self, request):
        pass

    # 로그아웃
    @staticmethod
    def get(request):
        logout(request)
        return redirect('/home')