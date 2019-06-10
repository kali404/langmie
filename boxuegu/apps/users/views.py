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

