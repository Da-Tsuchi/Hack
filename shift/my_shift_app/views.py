from django.shortcuts import render,redirect
from .day import *
from .forms import *

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
    return render(request, 'my_shift_app/index.html', {'form': form})

def table(request):
    year = request.session.get('year')
    month = request.session.get('month')

    # If the year and month data is in session
    days_with_weekday = get_days_with_weekday(year, month)
    return render(request, 'my_shift_app/table.html', {'days_with_weekday': days_with_weekday})