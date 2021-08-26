import hashlib
import json
import re

from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.http.response import HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django import views
from django.contrib.auth import logout
from django.utils.crypto import get_random_string
from ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

from .models import User, Post, PostLike, PostComment
from django.views.generic.list import ListView
from .utils import get_random_unicode
from django.views.decorators.csrf import csrf_exempt


class PostsView(ListView):
    model = Post
    paginate_by = 3
    context_object_name = 'posts'
    template_name = 'index.html'
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super(PostsView, self).get_context_data(**kwargs)
        user_pk = self.request.session.get('user')
        if user_pk:
            user = get_object_or_404(User, id=user_pk)
            if user.is_verified is True:
                context['user_id'] = user_pk
                context['profile_pic'] = self.request.session.get('profile_pic')
                context['likes'] = PostLike.objects.filter(user_id=user)
                return context
        return None


class UserDetailView(DetailView):
    model = User
    slug_field = "nickname"
    slug_url_kwarg = "nickname"
    template_name = 'mypage.html'

    def get_object(self, **kwargs):
        user = get_object_or_404(User, nickname=self.kwargs.get("nickname"))

        user_pk = self.request.session.get('user')
        if user_pk:
            return user
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user_pk = self.request.session.get('user')
        if user_pk:
            user = get_object_or_404(User, id=user_pk)
            if user.is_verified is True:
                context['user_id'] = user_pk
                return context
        return None


class Home(views.View):
    @staticmethod
    def post(request):
        return HttpResponseNotAllowed('get')

    @staticmethod
    def get(request):
        user_pk = request.session.get('user')  # 요청을 보낸 사용자의 세션 확인
        if user_pk:  # 세션이 비어있지 않다면
            return redirect('/')

        return redirect('/login')


class PostPage(views.View):
    @staticmethod
    def post(request):
        pass

    @staticmethod
    def get(request):
        email = request.session.get('email')
        if email:
            return HttpResponseNotAllowed('not allowed')
        user_pk = request.session.get('user')
        if not user_pk:
            return redirect('/login')

        post_id = request.GET['id']
        post = get_object_or_404(Post, id=post_id)

        comments = PostComment.objects.filter(post_id=post_id)
        profile_pic = request.session.get('profile_pic')
        context = {
            'post': post,
            'comments': comments,
            'profile_pic': profile_pic
        }
        return render(request, 'post.html', context)


class AddPost(views.View):
    @staticmethod
    @ratelimit(key='ip', rate='6/m')
    def post(request):
        email = request.session.get('email')
        if email:
            return HttpResponseNotAllowed('not allowed')
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
        email = request.session.get('email')
        if email:
            return HttpResponseNotAllowed('not allowed')
        user_pk = request.session.get('user')
        if user_pk:
            profile_pic = request.session.get('profile_pic')
            context = {'profile_pic': profile_pic}
            return render(request, 'add_post.html', context)
        return redirect('/login')


class Comment(views.View):
    @staticmethod
    @ratelimit(key='ip', rate='10/m')
    def post(request):
        email = request.session.get('email')
        if email:
            return HttpResponseNotAllowed('not allowed')
        user_pk = request.session.get('user')
        if user_pk:
            user = User.objects.get(id=user_pk)
        else:
            return redirect('/login')

        post_id = str(request.POST['post_id'])
        comment = request.POST['comment']

        if post_id and post_id != "" and comment and comment != "":
            post_comment = PostComment()
            post_comment.post_id = get_object_or_404(Post, id=post_id)
            post_comment.user_id = user
            post_comment.comment = comment
            post_comment.save()

            comment_model = PostComment.objects.filter(post_id=post_id).order_by('created_at')[0:3]
            user1 = ""
            comment1 = ""
            user2 = ""
            comment2 = ""
            user3 = ""
            comment3 = ""
            try:
                user1 = comment_model[0].user_id.nickname
                comment1 = comment_model[0].comment
                user2 = comment_model[1].user_id.nickname
                comment2 = comment_model[1].comment
                user3 = comment_model[2].user_id.nickname
                comment3 = comment_model[2].comment
            except IndexError:
                pass

            context = {
                'commentRes': "success",
                'comment1': comment1,
                'comment2': comment2,
                'comment3': comment3,
                'user1': user1,
                'user2': user2,
                'user3': user3
            }
        else:
            context = {'commentRes': "fail"}
        return HttpResponse(json.dumps(context), content_type="application/json")

    @staticmethod
    def get(request):
        email = request.session.get('email')
        if email:
            return HttpResponseNotAllowed('not allowed')
        user_pk = request.session.get('user')
        if not user_pk:
            return redirect('/login')
        post_id = request.GET['post_id']
        comments = PostComment.objects.filter(post_id=post_id)
        context = {'comments': comments}
        return HttpResponse(json.dumps(context), content_type="application/json")


class EditPost(views.View):
    @staticmethod
    def post(request):
        email = request.session.get('email')
        if email:
            return HttpResponseNotAllowed('not allowed')
        user_pk = request.session.get('user')
        if not user_pk:
            return redirect('/login')

        post_id = request.POST['id']
        post = get_object_or_404(Post, id=post_id)  # 게시글 테이블에서 정보 가져오기

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
        email = request.session.get('email')
        if email:
            return HttpResponseNotAllowed('not allowed')
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

        profile_pic = request.session.get('profile_pic')
        context = {
            'id': post_id,
            'image': post.image,
            'desc': post.description,
            'profile_pic': profile_pic
        }
        return render(request, 'edit_post.html', context)


class DeletePost(views.View):
    @staticmethod
    def post(request):
        email = request.session.get('email')
        if email:
            return HttpResponseNotAllowed('not allowed')
        user_pk = request.session.get('user')
        if not user_pk:
            return HttpResponseNotAllowed('login')

        post_id = request.POST['id']
        post = get_object_or_404(Post, id=post_id)

        confirm = request.POST['confirm']
        if confirm == "confirm":
            post.delete()
            context = {'deleteRes': 'success'}
            return HttpResponse(json.dumps(context), content_type="application/json")
        else:
            context = {'deleteRes': 'fail'}
            return HttpResponse(json.dumps(context), content_type="application/json")

    @staticmethod
    def get(request):
        return HttpResponseNotAllowed('POST')


@method_decorator(ratelimit(key='user_or_ip', rate='1/m', method='POST'), name='post')
class Login(views.View):
    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)  # 데이터베이스에서 user_id 에 해당하는 데이터 가져오기
            salted_password = str(user.salt) + str(password)  # 불러온 해당유저 데이터에서, 솔트값을 사용자 입력 값과 합침
            hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()  # 솔트값과 합쳐진 사용자 입력값을 해시

            if str(user.password) == str(hashed_password):
                request.session['user'] = user.id  # 로그인 성공!
                request.session['profile_pic'] = user.profile_pic.url
                if user.is_verified is False:
                    request.session['email'] = user.email
                context = {'loginRes': "success"}
                return HttpResponse(json.dumps(context), content_type="application/json")

            else:
                context = {'loginRes': "fail"}  # 비번 틀림
                return HttpResponse(json.dumps(context), content_type="application/json")
        else:
            context = {'loginRes': "fail"}  # 이메일 존재 안함
            return HttpResponse(json.dumps(context), content_type="application/json")

    @staticmethod
    def get(request):
        verified = request.session.get('verify')
        if verified:
            return redirect('/findpw')
        user_pk = request.session.get('user')  # 사용자 세션 확인
        if user_pk:  # 세션이 비지 않았다면?
            # 여기 왜 왔어~ 로그인 했으면 홈으로 돌아가~
            return redirect('/')

        # 로그인 하세요~
        return render(request, 'sign_in.html')  # 사용자에게 로그인 페이지 보여줌


class EmailVerify(views.View):
    @staticmethod
    def post(request):
        email = request.session.get('email')
        if not email:
            return HttpResponseBadRequest('invalid request')

        try:
            input_code = request.POST['code']
            name = None
        except:
            input_code = None
            name = request.POST['name']

        if input_code and len(input_code) == 6:
            verify_code = request.session.get('verify_code')
            if input_code == verify_code:
                user = get_object_or_404(User, email=email)
                user.is_verified = True
                user.email = email
                user.save()

                request.session['verify'] = user.id

                del request.session['verify_code']
                del request.session['email']

                context = {'verifyRes': "success"}
                return HttpResponse(json.dumps(context), content_type="application/json")
            tried = request.session.get('verify_tried')
            if tried:  # 10번 시도하면 로그아웃으로 세션 초기화
                tried = int(tried) + 1
                if tried >= 10:
                    logout(request)
                request.session['verify_tried'] = str(tried)
            else:
                request.session['verify_tried'] = "1"
            context = {'verifyRes': "fail"}
            return HttpResponse(json.dumps(context), content_type="application/json")

        elif email and name:
            if User.objects.filter(email=email, name=name).exists():
                verify_code = get_random_string(length=6, allowed_chars='1234567890')
                request.session['verify_code'] = verify_code
                spaced_code = verify_code[0:3] + ' ' + verify_code[3:6]
                email = EmailMessage(
                    f'{spaced_code} mini-instagram Verification code',
                    f'Your code is: {verify_code}',
                    to=[email]
                )
                email.send(fail_silently=False)

                context = {'email_send': "success"}
                return HttpResponse(json.dumps(context), content_type="application/json")
            else:
                context = {'email_send': "fail"}
                return HttpResponse(json.dumps(context), content_type="application/json")
        return HttpResponseBadRequest('invalid request.')

    @staticmethod
    def get(request):
        email = request.session.get('email')
        if email:
            if request.session.get('verify_code'):
                return render(request, 'verify_code.html')
            else:
                return render(request, 'email_verify.html', {'email': email, 'type': "first_verify"})

        user_pk = request.session.get('user')
        if user_pk:
            return redirect('/')
        return render(request, 'email_verify.html', {'type': "find_pw"})


class ResendEmail(views.View):
    @staticmethod
    def post(request):
        try:
            reset = request.POST['reset_verify']
        except:
            return HttpResponseBadRequest('')

        user_pk = request.session.get('user')
        email = request.session.get('email')
        verified = None
        if not user_pk:
            verified = request.session.get('verify')

        if email or verified:
            if reset == "reset":
                del request.session['verify_code']
                context = {'resetRes': "success"}
                return HttpResponse(json.dumps(context), content_type="application/json")
        return HttpResponseNotAllowed

    @staticmethod
    def get(request):
        return HttpResponseNotAllowed('post')


class LogOut(views.View):
    @staticmethod
    def post(request):
        return HttpResponseNotAllowed('GET')

    # 로그아웃
    @staticmethod
    def get(request):
        logout(request)
        return redirect('/login')


class SignUp(views.View):
    @staticmethod
    def post(request):
        email = request.session.get('email')
        if email:
            return HttpResponseNotAllowed('not allowed')

        try:
            name = str(request.POST['name'])
            nickname = str(request.POST['nickname'])
            email = str(request.POST['email'])
            password = str(request.POST['password'])
            password_chk = str(request.POST['password-check'])
        except:
            return HttpResponseBadRequest('invalid request')

        if User.objects.filter(nickname=nickname).exists():
            return HttpResponse(json.dumps({'SignupRes': "nickname_exists"}), content_type="application/json")
        if User.objects.filter(email=email).exists():
            return HttpResponse(json.dumps({'SignupRes': "email_exists"}), content_type="application/json")
        if password_chk != password:
            return HttpResponse(json.dumps({'SignupRes': "pw_fail"}), content_type="application/json")

        if not len(name) > 0:
            return HttpResponse(json.dumps({'SignupRes': "name_short"}), content_type="application/json")
        if not 4 < len(nickname):
            return HttpResponse(json.dumps({'SignupRes': "nickname_short"}), content_type="application/json")
        if not len(nickname) < 15:
            return HttpResponse(json.dumps({'SignupRes': "nickname_long"}), content_type="application/json")
        if not len(email) > 3:
            return HttpResponse(json.dumps({'SignupRes': "email_short"}), content_type="application/json")
        if not len(password) >= 4:
            return HttpResponse(json.dumps({'SignupRes': "pw_long"}), content_type="application/json")

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, email):
            return HttpResponse(json.dumps({'SignupRes': "invalid_email"}), content_type="application/json")
        regex = r'^([a-z0-9_](?:(?:[a-z0-9_]|(?:\.(?!\.))){0,13}(?:[a-z0-9_]))?)$'
        if not re.fullmatch(regex, nickname):
            return HttpResponse(json.dumps({'SignupRes': "invalid_nickname"}), content_type="application/json")

        user = User()
        user.name = name
        user.nickname = nickname
        user.email = email
        salt = get_random_unicode(10)
        user.salt = salt
        salted_password = str(salt) + str(password)
        user.password = hashlib.sha256(salted_password.encode()).hexdigest()
        user.save()

        context = {'SignupRes': "success"}
        return HttpResponse(json.dumps(context), content_type="application/json")

    @staticmethod
    def get(request):
        user_pk = request.session.get('user')
        if user_pk:
            return redirect('/')
        return render(request, 'sign_up.html')


class MyPage(views.View):
    @staticmethod
    def post(request):
        pass

    @staticmethod
    def get(request):
        email = request.session.get('email')
        if email:
            return HttpResponseNotAllowed('not allowed')
        user_pk = request.session.get('user')
        if user_pk:
            user = User.objects.get(id=user_pk)
            context = {
                'user': user,
            }
            return render(request, 'mypage.html', context)
        return redirect('/login')


class SettingPage(views.View):
    @staticmethod
    def post(request):
        user_pk = request.session.get('user')
        if not user_pk:
            return HttpResponseNotAllowed('login')
        try:
            name = request.POST['name']
            nickname = request.POST['nickname']
            email = request.POST['email']
            introduce = request.POST['intro']
        except:
            return HttpResponse(json.dumps({'settingRes': "fail"}), content_type="application/json")
        user = get_object_or_404(User, id=user_pk)
        recent_name = user.name
        recent_nickname = user.nickname
        recent_email = user.email
        recent_introduce = user.introduce
        if recent_name != name:
            user.name = name
        if recent_nickname != nickname:
            user.nickname = nickname
        if recent_introduce != introduce:
            user.introduce = introduce
        if recent_email != email:
            user.is_verified = False
            request.session['email'] = email
        user.save()
        return HttpResponse(json.dumps({'settingRes': "success"}), content_type="application/json")

    @staticmethod
    def get(request):
        email = request.session.get('email')
        if email:
            return HttpResponseNotAllowed('not allowed')
        user_pk = request.session.get('user')
        if user_pk:
            user = User.objects.get(id=user_pk)
            profile_pic = request.session.get('profile_pic')
            context = {
                'user': user,
                'profile_pic': profile_pic
            }
            return render(request, 'setting_profil.html', context)
        return redirect('/login')


class ChangePwPage(views.View):
    @staticmethod
    def post(request):
        user_pk = request.session.get('user')
        verified = request.session.get('verify')
        if user_pk:
            try:
                password = str(request.POST['password'])
                new_password = str(request.POST['new-password'])
                new_password_chk = str(request.POST['new-password-check'])
            except:
                return HttpResponseBadRequest('invalid request')
            user = get_object_or_404(User, id=user_pk)
            salted_password = str(user.salt) + str(password)
            hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()

            if str(user.password) != str(hashed_password):
                return HttpResponse(json.dumps({'changepwRes': "fail"}), content_type="application/json")
        elif verified:
            try:
                new_password = str(request.POST['password'])
                new_password_chk = str(request.POST['password-check'])
            except:
                return HttpResponseBadRequest('invalid request')
            user = get_object_or_404(User, id=verified)
        else:
            return HttpResponseNotAllowed('not allowed')

        if new_password == new_password_chk:
            salt = get_random_unicode(10)
            salted_new_password = str(salt) + str(new_password)
            hashed_new_password = hashlib.sha256(salted_new_password.encode()).hexdigest()
            user.salt = salt
            user.password = hashed_new_password
            user.save()
            try:
                del request.session['verify']
            except:
                pass
            return HttpResponse(json.dumps({'changepwRes': "success"}), content_type="application/json")
        else:
            return HttpResponse('new password is different')

    @staticmethod
    def get(request):
        email = request.session.get('email')
        if email:
            return HttpResponseNotAllowed('not allowed')
        user_pk = request.session.get('user')
        if user_pk:
            profile_pic = request.session.get('profile_pic')
            context = {
                'profile_pic': profile_pic
            }
            return render(request, 'setting_passwd.html', context)
        return redirect('/login')


class FindingPwPage(views.View):
    @staticmethod
    def post(request):
        email = str(request.POST['email'])
        name = str(request.POST['name'])

        if User.objects.filter(email=email, name=name).exists():
            user = User.objects.get(email=email)
            if user.name != name:
                return HttpResponse(json.dumps({'findingpwRes': "fail"}), content_type="application/json")
            verified = request.session.get('verify')
            if verified:
                return HttpResponseBadRequest('already verified')
            else:
                user.is_verified = False
                user.save()
                request.session['email'] = email
                return HttpResponse(json.dumps({'findingpwRes': "success"}), content_type="application/json")

    @staticmethod
    def get(request):
        verified = request.session.get('verify')
        if verified:
            return render(request, 'change_lost_pw.html')
        user_pk = request.session.get('user')
        if user_pk:
            return HttpResponseNotAllowed('already logined')
        return render(request, 'email_verify.html', {'is_finding_pw': "1"})


class AddHeart(views.View):
    @staticmethod
    def post(request):
        user_pk = request.session.get('user')
        if not user_pk:
            return HttpResponseNotAllowed('login')

        post_id = request.POST['post_id']

        like = request.session.get(f'post{post_id}')
        post = get_object_or_404(Post, id=post_id)
        if like:
            like = str(int(like) + 1)
        else:
            user = get_object_or_404(User, id=user_pk)
            if PostLike.objects.filter(user_id=user, post_id=post).exists():
                like = "2"
            else:
                like = "1"
        request.session[f'post{post_id}'] = like

        user = get_object_or_404(User, id=user_pk)
        if int(like) % 2 == 0:
            PostLike.objects.filter(user_id=user, post_id=post).delete()
        else:
            PostLike.objects.filter(user_id=user, post_id=post).delete()
            post_like = PostLike()
            post_like.post_id = post
            post_like.user_id = user
            post_like.save()

        return HttpResponse(json.dumps({'r': "s"}), content_type="application/json")

    @staticmethod
    def get(request):
        return HttpResponseNotAllowed('post')


class CheckHeart(views.View):
    @staticmethod
    @ratelimit(key='post:post_id', rate='10/m')
    def post(request, *args):
        user_pk = request.session.get('user')
        if not user_pk:
            return HttpResponseNotAllowed('login')
        post_id = request.POST['post_id']
        post = get_object_or_404(Post, id=post_id)
        user = get_object_or_404(User, id=user_pk)
        if PostLike.objects.filter(user_id=user, post_id=post).exists():
            return HttpResponse(json.dumps({'r': "y"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'r': "n"}), content_type="application/json")

    @staticmethod
    def get(request):
        return HttpResponseNotAllowed('post')
