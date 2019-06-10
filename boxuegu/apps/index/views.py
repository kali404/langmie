from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.shortcuts import render
from django.views import View
from user_test.form import RegisterForm
from django.http import HttpResponse
from users.models import Banner
from .models import *
from courses.models import Course, CourseOrg


class IndexView(View):
    def get(self, request):
        kecheng = Banner.objects.all()
        all_banners = [i for i in kecheng]

        courses = Course.objects.all()
        banner_courses = Course.objects.all()
        course_orgs = CourseOrg.objects.all()

        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
            'MEDIA_URL':settings.MEDIA_URL
        })

