from django.shortcuts import render
from .day import *

# Create your views here.
# def index(request):
#     context = {'list':["data1","data2"]}
#     return render(request, 'my_shift_app/index.html',context)

def index(request):
    if request.method == "POST":
        year = int(request.POST.get('year'))
        month = int(request.POST.get('month'))
        days_with_weekday = get_days_with_weekday(year, month)
        return render(request, 'my_shift_app/index.html', {'days_with_weekday': days_with_weekday})
    else:
        return render(request, 'my_shift_app/index.html')