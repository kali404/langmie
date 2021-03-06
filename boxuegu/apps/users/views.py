from django.conf import settings
from django.http import JsonResponse
from pure_pagination import Paginator
from courses.models import Course
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from utils.mixin_utils import LoginRequiredMixin
from utils.boxuegu_sig import dumps, loads
from django.contrib.auth import login, logout, authenticate
from django.db import DatabaseError
from django.shortcuts import render, redirect, reverse
from django.views import View
from .models import UserProfile, EmailVerifyRecord
from .forms import RegisterForm, LoginForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from celery_tasks.email.tasks import send_user_mali


class RegisterView(View):
    """
        展示注册页面
    """

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {
            'register_form': register_form,
        })

    def post(self, request):
        data = request.POST
        register_form = RegisterForm(data)  # 生成数据对象
        res = register_form.is_valid()  # 验证
        if res:
            email = register_form.cleaned_data.get('email')
            pwd = register_form.cleaned_data.get('password')
            if UserProfile.objects.filter(email=email).count() > 0:
                return render(request, 'register.html', {'register_form': register_form, 'msg': '该邮箱用户已经注册!'})
            try:
                user = UserProfile.objects.create_user(email=email, password=pwd, username=email)
            except DatabaseError:
                return render(request, 'register.html', {'register_form': register_form, 'msg': '注册失败!'})
            login(request, user)
            return redirect('/')

        return render(request, 'register.html', {'register_form': register_form})


class LogIn(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        data = request.POST
        login_form = LoginForm(data)
        res = login_form.is_valid()
        if res:
            name = login_form.cleaned_data.get('username')
            pwd = login_form.cleaned_data.get('password')
            user = authenticate(request, username=name, password=pwd)
            if user is None:
                return render(request, 'login.html', {'form_errors': login_form})

            login(request, user)
            return redirect("/")
        return render(request, 'login.html', {'form_errors': login_form})


class LogOut(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class ForGet(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        data = request.POST
        code = data.get('captcha_1')
        send_type = 'forget'
        forgetform = ForgetForm(data)
        res = forgetform.is_valid()
        if res:
            email = forgetform.cleaned_data.get('email')
            try:
                user = UserProfile.objects.get(email=email)
            except:
                return render(request, 'forgetpwd.html', {'msg': '该邮箱没注册'})
            # 加密
            try:
                EmailVerifyRecord.objects.create(code=code, email=email, send_type=send_type)
            except:
                return render(request, 'forgetpwd.html', {'msg': '存入验证信息出错'})

            token = dumps({'email': email, 'code': code, 'send_type': send_type}, 60 * 60 * 10)
            urls = settings.EMAIL_ACTIVE_URL + token
            send_user_mali.delay(email, urls)
            return render(request, 'send_success.html')
        return render(request, 'forgetpwd.html', {'forget_form': forgetform})


class ResetView(View):
    def get(self, request):
        active_code = request.GET.get('active_code')
        if active_code is None:
            render(request, 'forgetpwd.html', {'msg': '接收参数错误!'})
        data = loads(active_code, 60 * 60 * 10)
        if data is None:
            return render(request, 'forgetpwd.html', {'msg': '解析失败!'})
        email = data.get('email')

        try:
            user = UserProfile.objects.get(email=email)
        except:
            return render(request, 'forgetpwd.html', {'msg': '未知错误!'})

        return render(request, 'password_reset.html', {'email': email})

    def post(self, request):
        data = request.POST
        modifypwdform = ModifyPwdForm(data)
        res = modifypwdform.is_valid()

        if res:
            email = modifypwdform.cleaned_data.get('email')
            pwd = modifypwdform.cleaned_data.get('password1')
            print(email)
            try:
                user = UserProfile.objects.get(email=email)
            except:
                return render(request, 'password_reset.html', {'modify_form': {'errors': '查无此用户'}})
            user.set_password(pwd)
            user.save()
            return redirect('/')
        return render(request, 'password_reset.html', {'modify_form': {'errors': '参数错误'}})


class UserInfo(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html', {'MEDIA_URL': settings.MEDIA_URL})

    def post(self, request):
        data = request.POST
        user_form = UserInfoForm(data, instance=request.user)
        res = user_form.is_valid()
        if res:
            request.user.save()
            return redirect('users/info/')
        return render(request, 'usercenter-info.html', {'MEDIA_URL': settings.MEDIA_URL,
                                                        'status': '修改失败'})


class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        data = request.POST
        image_form = UploadImageForm(data, request.FILES, instance=request.user)
        res = image_form.is_valid()

        if res:
            request.user.save()
            return JsonResponse({"status": "success", "msg": "头像修改成功"})
        return JsonResponse({
            "status": "success",
            "msg": '头像修改失败'
        })


class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses,
            'MEDIA_URL': settings.MEDIA_URL
        })


class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        data = UserFavorite.objects.filter(fav_type=2, user=user.id, )
        org_list = [CourseOrg.objects.get(id=i.fav_id) for i in data]
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
            'MEDIA_URL': settings.MEDIA_URL
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        data = UserFavorite.objects.filter(fav_type=3, user=user.id, )
        teacher_list = [Teacher.objects.get(id=i.fav_id) for i in data]
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
            'MEDIA_URL': settings.MEDIA_URL
        })


class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        data = UserFavorite.objects.filter(fav_type=1, user=user.id, )
        course_id = [Course.objects.get(id=i.fav_id) for i in data]
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_id,
            'MEDIA_URL': settings.MEDIA_URL
        })


class MyMessageView(LoginRequiredMixin, View):
    def get(self, request):
        messages = UserMessage.objects.filter(user=request.user.id)
        paginator = Paginator(messages, 1)
        page_mun = request.GET.get('page', 1)
        messages = paginator.page(page_mun)

        return render(request, 'usercenter-message.html', {
            'messages': messages,
        })


class Gut(View):
    pass
