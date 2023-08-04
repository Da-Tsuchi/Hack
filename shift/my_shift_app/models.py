from django.db import models

# Create your models here.

# class Teacher(models.Model):
#     name = models.CharField(max_length=200)

# class Student(models.Model):
#     name = models.CharField(max_length=200)
    
class Teacher(models.Model):
    teacher_number = models.IntegerField(primary_key=True)  # 追加したフィールド
    name = models.CharField(max_length=200)  # 名前

class Student(models.Model):
    student_number = models.IntegerField(primary_key=True) # 生徒番号
    name = models.CharField(max_length=200)  # 名前
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)# 講師番号