from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
# from .views import ShiftsSpreadsheetView

app_name = 'my_shift_app'
urlpatterns = [
    # path('', views.index, name='index'),
    path("", views.index, name="index"),
    path("table/", views.table, name="table"),
    path('login/', views.Login, name='login'),
    path('manage/', views.manage, name='manage'),
    path('teacher/', views.teacher, name='teacher'),
    path('student/', views.student, name='student'),
    path('shift_manage/', views.shift_manage, name='shift_manage'),
]