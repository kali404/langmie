from django.shortcuts import render
from django.views import View


class Coures_List(View):
    def get(self):
        pass


class Tre(View):
    def get(self):
        pass



class Mycoures(View):
    def get(self,request):
        return render(request,'usercenter-mycourse.html')