from django.urls import path
from . import views

app_name = 'my_shift_app'
urlpatterns = [
    # path('', views.index, name='index'),
    path("", views.index, name="index"),
    path("table/", views.table, name="table"),
    path("get_teachers/", views.get_teachers, name="get_teachers"),
    path("get_students/", views.get_students, name="get_students"),
]