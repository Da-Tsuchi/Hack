from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from calendar import monthrange

    
class Teacher(models.Model):
    teacher_number = models.IntegerField(primary_key=True)  # 追加したフィールド
    name = models.CharField(max_length=200)  # 名前

class Student(models.Model):
    student_number = models.IntegerField(primary_key=True) # 生徒番号
    name = models.CharField(max_length=200)  # 名前
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)# 講師番号
    
class StudentFirstSchedule(models.Model):
    year = models.IntegerField(validators=[MinValueValidator(2023), MaxValueValidator(9999)],default=2023)
    month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    student = models.ForeignKey(Student, on_delete=models.CASCADE)# 生徒番号(外部キー制約)
      
class StudentSecondSchedule(models.Model):
    year = models.IntegerField(validators=[MinValueValidator(2023), MaxValueValidator(9999)],default=2023)
    month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    student = models.ForeignKey(Student, on_delete=models.CASCADE)# 生徒番号(外部キー制約)
    
class TeacherSchedule(models.Model):
    year = models.IntegerField(validators=[MinValueValidator(2023), MaxValueValidator(9999)],default=2023)
    month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)# 生徒番号(外部キー制約)
    
    

