from django.shortcuts import render

# Create your views here.
def index(request):
    context = {'list':["data1","data2"]}
    return render(request, 'my_shift_app/index.html',context)