from django.shortcuts import render,redirect
from .day import *
from .forms import *
from .models import *
from django.views import View

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from calendar import monthrange

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
def student_schedule(request):
    # 生徒情報の登録処理...
    if request.method == 'POST':
        formFirst = StudentFirstScheduleForm(request.POST)
        formSecond = StudentSecondScheduleForm(request.POST)
        if formFirst.is_valid():
            formFirst.save()
            return redirect('my_shift_app:student_schedule')
        if formSecond.is_valid():
            formSecond.save()
            return redirect('my_shift_app:student_schedule')
    else:
        formFirst = StudentFirstScheduleForm()
        formSecond = StudentSecondScheduleForm()
    students_first = StudentFirstSchedule.objects.all()
    students_second = StudentSecondSchedule.objects.all()
    return render(request, 'my_shift_app/student_schedule.html', {'formFirst': formFirst,"formSecond":formSecond, 'students_first': students_first,"students_second":students_second})

@login_required
def student_first_schedule(request):
    # 生徒情報の登録処理...
    if request.method == 'POST':
        formFirst = StudentFirstScheduleForm(request.POST)
        if formFirst.is_valid():
            formFirst.save()
            return redirect('my_shift_app:student_schedule')
    else:
        formFirst = StudentFirstScheduleForm()
    students_first = StudentFirstSchedule.objects.all()
    return render(request, 'my_shift_app/student_schedule.html', {'formFirst': formFirst,'students_first': students_first})

@login_required
def student_second_schedule(request):
    # 生徒情報の登録処理...
    if request.method == 'POST':
        formSecond = StudentSecondScheduleForm(request.POST)
        if formSecond.is_valid():
            formSecond.save()
            return redirect('my_shift_app:student_schedule')
    else:
        formSecond = StudentSecondScheduleForm()
    students_second = StudentSecondSchedule.objects.all()
    return render(request, 'my_shift_app/student_schedule.html', {"formSecond":formSecond, "students_second":students_second})

@login_required
def shift_manage(request):
    if request.method == 'POST':
        form = MonthYearForm(request.POST)
        if form.is_valid():
            year = int(form.cleaned_data['year'])
            month = int(form.cleaned_data['month'])
            # shifts = [Shift(day=i+1) for i in range(num_days)]  # create a Shift instance for each day
            days_with_weekday = get_days_with_weekday(year, month)
            students = Student.objects.all()
            

            # 指定した年と月の日数を取得します
            _, num_days = monthrange(year, month)
            
            return render(request, 'my_shift_app/shift_table.html', {'year': year, 'month': month,"days_with_weekday":days_with_weekday,"students":students})
    else:
        form = MonthYearForm()
    return render(request, 'my_shift_app/shift_manage.html', {'form': form})

@login_required
def shift_view(request):
    if request.method == 'POST':
        year = request.session.get('year')
        month = request.session.get('month')
        student_numbers = request.POST.getlist('student')
        days_with_weekday = get_days_with_weekday(year, month)

        for day, student_number in zip(days_with_weekday, student_numbers):
            if student_number:  # 学生が選択されている場合のみデータを保存
                student = Student.objects.get(student_number=student_number)

                # StudentFirstScheduleとStudentSecondScheduleにデータを保存
                StudentFirstSchedule.objects.create(year =year,month=month,day =day, student=student)
                StudentSecondSchedule.objects.create(year =year,month=month,day =day, student=student)

        return redirect('schift_view_student')  # データ保存後、スケジュールページにリダイレクト

    else:
        students = Student.objects.all()
        dates = [date for date in generate_dates()]  # generate_datesは適切な日付を生成する関数
        return render(request, 'my_shift_app/schift_view.html', {'students': students})
