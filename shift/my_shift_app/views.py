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
from .teacher_decision import *
# from django.template.loader import render_to_string
# from weasyprint import HTML
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
        # If the year and month data is in session
    days_with_weekday = get_days_with_weekday(year, month)   
    if request.method == 'POST':
        form = TeacherRequestForm(request.POST)

        print(request.POST)
        print(form.errors)
        if form.is_valid():
            selected_teacher = form.cleaned_data['teacher']
            year = form.cleaned_data['year']
            month = form.cleaned_data['month']
            print(selected_teacher)

            for day, _ in days_with_weekday:
                shift_status = request.POST.get(f'{day}_shift')
                print(shift_status)
                if shift_status == 'OK':
                    TeacherSchedule.objects.create(year=year, month=month, day=day, teacher=selected_teacher)
                        
            return redirect('my_shift_app:index')  # 適切なリダイレクト先へ変更
            # 他の処理
            
    else:
        form = TeacherRequestForm()
        

    teacherRequests = TeacherSchedule.objects.all()
                    

    return render(request, 'my_shift_app/table.html', {'days_with_weekday': days_with_weekday,"year":year,"month":month, 'form': form, 'teacherRequests': teacherRequests})


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
        print(request.POST)
        form = TeacherForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
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

# シフト作成の年月選択画面
@login_required
def shift_manage(request):
    if request.method == 'POST':
        form = MonthYearForm(request.POST)
        if form.is_valid():
            
            year = int(form.cleaned_data['year'])
            month = int(form.cleaned_data['month'])
            # shifts = [Shift(day=i+1) for i in range(num_days)]  # create a Shift instance for each day
            request.session['year'] = year
            request.session['month'] = month
            
            students = Student.objects.all()
            # 指定した年と月の日数を取得します
            _, num_days = monthrange(year, month)
            
            return redirect('my_shift_app:shift_table')
            # return render(request, 'my_shift_app/shift_table.html', {'year': year, 'month': month,"days_with_weekday":days_with_weekday,"students":students})
    else:
        form = MonthYearForm()
    return render(request, 'my_shift_app/shift_manage.html', {'form': form})

# 一覧画面で生徒の授業日程を選択
@login_required
def shift_table(request):
    
    year = request.session.get('year')
    month = request.session.get('month')
    students = Student.objects.all()

    days_with_weekday = get_days_with_weekday(year, month)
    if request.method == 'POST':
        for key, values in request.POST.lists():
            if key.startswith('student_first_'):
                day = key.replace('student_first_', '').replace('[]', '')
                if len(values) != len(set(values)):
                    return HttpResponse('同じ生徒を同じ日に複数回選ぶことはできません。', status=400)
                for value in values:
                    student_number = value
                    if student_number:
                        student = Student.objects.get(student_number=student_number)
                        schedule = StudentFirstSchedule(year =year,month=month,day =day, student=student)
                        schedule.save()
            if key.startswith('student_second_'):
                day = key.replace('student_second_', '').replace('[]', '')
                if len(values) != len(set(values)):
                    return HttpResponse('同じ生徒を同じ日に複数回選ぶことはできません。', status=400)
                for value in values:
                    student_number = value
                    if student_number:
                        student = Student.objects.get(student_number=student_number)
                        schedule = StudentSecondSchedule(year =year,month=month,day =day, student=student)
                        schedule.save()
        return redirect('my_shift_app:shift_teacher')
        
    return render(request, 'my_shift_app/shift_table.html', {'year': year, 'month': month,"days_with_weekday":days_with_weekday,"students":students})  # データ保存後、スケジュールページにリダイレクト
    
# 生徒に応じて講師を選択
@login_required
def shift_teacher(request):
    year = request.session.get('year')
    month = request.session.get('month')
    days_with_weekday = get_days_with_weekday(year, month)
    students = Student.objects.all()
    teachers = Teacher.objects.all()
    
    days =[]
    weekday=[]
    for n in range(0, calendar.monthrange(int(year), int(month))[1] ):
        days.append(days_with_weekday[n][0])
        weekday.append(days_with_weekday[n][1])
        
    schedulesFirst = []
    schedulesSecond = []
    TeacherRequest = []
    # シフトに入れる人の中で生徒担当が多い人を選ぶアルゴリズム
    cnt_list = []
    for day in range(1, calendar.monthrange(int(year), int(month))[1] + 1):
        schedulesFirst.append(list(StudentFirstSchedule.objects.filter(year=year, month=month, day=day).values_list('student', flat=True))) 
        schedulesSecond.append(list(StudentSecondSchedule.objects.filter(year=year, month=month, day=day).values_list('student', flat=True)))
        TeacherRequest.append(list(TeacherSchedule.objects.filter(year=year, month=month, day=day).values_list('teacher', flat=True)))
        cnt_list.append(teacher_decision(year, month, day))
    # print(cnt_list)
    print(TeacherRequest)
    
    teacher_num_cnt = []
    # print(cnt_list)
    for day in cnt_list:
        # print(day)
        sorted_cnt_list = sorted(day.items(), key=lambda item: item[1])
        teacher_numbers = [item[0] for item in sorted_cnt_list]
        teacher_numbers.reverse()
        teacher_num_cnt.append(teacher_numbers)
    print(teacher_num_cnt)

    t  = list(zip(TeacherRequest,teacher_num_cnt))

    matched_t = []
    unmatched_t =[]

    for teacher_request,cnt_by_day in t:
        matched_teachers = [t for t in cnt_by_day if t in teacher_request]
        unmatched_teachers = [t for t in teacher_request if t not in matched_teachers]
        matched_t.append(matched_teachers)
        unmatched_t.append(unmatched_teachers)
    
    print(matched_t)
    print(unmatched_t)
    # zipがHTMLで使えないので、リストに変換
    schedule = list(zip(days,weekday,matched_t ,unmatched_t,schedulesFirst, schedulesSecond))
    
    context = {
        'year': year,
        'month': month,
        "days_with_weekday": days_with_weekday,
        "students": students,
        "teachers": teachers,
        "schedule": schedule,
        # その他のコンテキスト変数...
        'matched_t': matched_t,
        'unmatched_t': unmatched_t,
    }

    if request.method == 'POST':
        selected_teachers_for_days = {}  # This will hold day as key and selected teachers as value

        for key, values in request.POST.lists():
            if key.startswith('teacher_'):
                day = key.replace('teacher_', '').replace('[]', '')
                if len(values) != len(set(values)):
                    return HttpResponse('同じ先生を同じ日に複数回選ぶことはできません。', status=400)

                selected_teachers_for_days[day] = values

        # セッションに選択された教師番号を保存
        request.session['selected_teachers_for_days'] = selected_teachers_for_days

        return redirect('my_shift_app:shift_confirm')

    return render(request, 'my_shift_app/shift_teacher.html', context)

def shift_confirm(request):
    year = request.session.get('year')
    month = request.session.get('month')
    days_with_weekday = get_days_with_weekday(year, month)
    students = Student.objects.all()
    teachers = Teacher.objects.all()
    
    days =[]
    weekday=[]
    for n in range(0, calendar.monthrange(int(year), int(month))[1] ):
        days.append(days_with_weekday[n][0])
        weekday.append(days_with_weekday[n][1])
        
    schedulesFirst = []
    schedulesSecond = []
    TeacherRequest = []
    # シフトに入れる人の中で生徒担当が多い人を選ぶアルゴリズム
    cnt_list = []
    for day in range(1, calendar.monthrange(int(year), int(month))[1] + 1):
        schedulesFirst.append(list(StudentFirstSchedule.objects.filter(year=year, month=month, day=day).values_list('student', flat=True))) 
        schedulesSecond.append(list(StudentSecondSchedule.objects.filter(year=year, month=month, day=day).values_list('student', flat=True)))
        TeacherRequest.append(list(TeacherSchedule.objects.filter(year=year, month=month, day=day).values_list('teacher', flat=True)))
        cnt_list.append(teacher_decision(year, month, day))
    # print(cnt_list)
    print(TeacherRequest)
    
    selected_teachers_for_days = request.session.get('selected_teachers_for_days', {})
    print(selected_teachers_for_days)
    
    teacher_names_for_days = []
    for day, teacher_numbers in selected_teachers_for_days.items():
        print(teacher_numbers)
        if(teacher_numbers == [""]):
            teacher_names = [""]
        else:
            teacher_names = [Teacher.objects.get(teacher_number=tn).name for tn in teacher_numbers]
        teacher_names_for_days.append(teacher_names)
    
    # zipがHTMLで使えないので、リストに変換
    schedule = list(zip(days,weekday,teacher_names_for_days,schedulesFirst, schedulesSecond))
    
    context = {
        'year': year,
        'month': month,
        "days_with_weekday": days_with_weekday,
        "students": students,
        "teachers": teachers,
        "schedule": schedule,
        'teacher_names_for_days': teacher_names_for_days,
    }
    
    return render(request, 'my_shift_app/shift_confirm.html',context)

def shift_pdf(request):
    year = request.session.get('year')
    month = request.session.get('month')
    days_with_weekday = get_days_with_weekday(year, month)
    students = Student.objects.all()
    teachers = Teacher.objects.all()
    
    days =[]
    weekday=[]
    for n in range(0, calendar.monthrange(int(year), int(month))[1] ):
        days.append(days_with_weekday[n][0])
        weekday.append(days_with_weekday[n][1])
        
    schedulesFirst = []
    schedulesSecond = []
    TeacherRequest = []
    # シフトに入れる人の中で生徒担当が多い人を選ぶアルゴリズム
    cnt_list = []
    for day in range(1, calendar.monthrange(int(year), int(month))[1] + 1):
        schedulesFirst.append(list(StudentFirstSchedule.objects.filter(year=year, month=month, day=day).values_list('student', flat=True))) 
        schedulesSecond.append(list(StudentSecondSchedule.objects.filter(year=year, month=month, day=day).values_list('student', flat=True)))
        TeacherRequest.append(list(TeacherSchedule.objects.filter(year=year, month=month, day=day).values_list('teacher', flat=True)))
        cnt_list.append(teacher_decision(year, month, day))
    # print(cnt_list)
    print(TeacherRequest)
    
    selected_teachers_for_days = request.session.get('selected_teachers_for_days', {})
    print(selected_teachers_for_days)
    
    teacher_names_for_days = []
    for day, teacher_numbers in selected_teachers_for_days.items():
        print(teacher_numbers)
        if(teacher_numbers == [""]):
            teacher_names = [""]
        else:
            teacher_names = [Teacher.objects.get(teacher_number=tn).name for tn in teacher_numbers]
        teacher_names_for_days.append(teacher_names)
    
    # zipがHTMLで使えないので、リストに変換
    schedule = list(zip(days,weekday,teacher_names_for_days,schedulesFirst, schedulesSecond))
    
    context = {
        'year': year,
        'month': month,
        "days_with_weekday": days_with_weekday,
        "students": students,
        "teachers": teachers,
        "schedule": schedule,
        'teacher_names_for_days': teacher_names_for_days,
    }
    
    # この部分でHTMLテンプレートを文字列としてレンダリング
    year = request.session.get('year')
    month = request.session.get('month')
    days_with_weekday = get_days_with_weekday(year, month)
    students = Student.objects.all()
    teachers = Teacher.objects.all()

    # ... 以下、shift_confirmの中のcontext生成ロジックをコピー ...

    context = {
        'year': year,
        'month': month,
        "days_with_weekday": days_with_weekday,
        "students": students,
        "teachers": teachers,
        "schedule": schedule,
        'teacher_names_for_days': teacher_names_for_days,
    }
    
    html_string = render_to_string('my_shift_app/shift_confirm.html',context)

    # WeasyPrintを使用してPDFを生成
    html = HTML(string=html_string)
    pdf_file = html.write_pdf()

    # PDFをHTTPレスポンスとして返す
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    return response