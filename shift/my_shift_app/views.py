from django.shortcuts import render,redirect
from .day import *
from .forms import *
from .models import *
from django.views import View

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

import csv

def index(request):

    if request.method == "POST":
        form = MonthYearForm(request.POST)
        if form.is_valid():
            year = int(form.cleaned_data['year'])
            month = int(form.cleaned_data['month'])
            request.session['year'] = year
            request.session['month'] = month
            return redirect('my_shift_app:table') # Redirect to the new view
    else:
        form = MonthYearForm()
        
    context = {
        'form': form
        # 他のコンテキスト変数
    }
    return render(request, 'my_shift_app/index.html',context)

def table(request):
    year = request.session.get('year')
    month = request.session.get('month')
    # 他のコード
    teachers = list(Teacher.objects.values_list('name', flat=True))
    students = list(Student.objects.values_list('name', flat=True))
                    
    # If the year and month data is in session
    days_with_weekday = get_days_with_weekday(year, month)
    return render(request, 'my_shift_app/table.html', {'days_with_weekday': days_with_weekday,"year":year,"month":month,"teachers":teachers,"students":students})


def Login(request):
# POST
    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
        ID = request.POST.get('userid')
        Pass = request.POST.get('password')

        # Djangoの認証機能
        user = authenticate(username=ID, password=Pass)

        # ユーザー認証
        if user:
            #ユーザーアクティベート判定
            if user.is_active:
                # ログイン
                login(request,user)
                # ホームページ遷移
                return HttpResponseRedirect(reverse('my_shift_app:manage'))
            else:
                # アカウント利用不可
                return HttpResponse("アカウントが有効ではありません")
        # ユーザー認証失敗
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    # GET
    else:
        return render(request, 'my_shift_app/login.html')

@login_required
def manage(request):
    return render(request, 'my_shift_app/manage.html')

@login_required
def teacher(request):
    # 先生情報の登録処理...
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('my_shift_app:teacher')
    else:
        form = TeacherForm()
    teachers = Teacher.objects.all()
    return render(request, 'my_shift_app/teacher.html', {'form': form, 'teachers': teachers})

@login_required
def student(request):
    # 生徒情報の登録処理...
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('my_shift_app:student')
    else:
        form = StudentForm()
    students = Student.objects.all()
    return render(request, 'my_shift_app/student.html', {'form': form, 'students': students})

@login_required
def shift_manage(request):
    # データベースから情報を取得し、セレクトボックスに表示...
    teachers = Teacher.objects.all()
    students = Student.objects.all()
    return render(request, 'my_shift_app/shift_manage.html', {'teachers': teachers, 'students': students})
