from django.shortcuts import render,redirect
from .day import *
from .forms import *
from .models import Teacher, Student

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

def get_teachers(request):
    teachers = Teacher.objects.all().values('id', 'name')
    teachers_list = list(teachers)
    return JsonResponse(teachers_list, safe=False)

def get_students(request):
    students = Student.objects.all().values('id', 'name')
    students_list = list(students)
    return JsonResponse(students_list, safe=False)