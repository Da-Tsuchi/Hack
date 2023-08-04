from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from calendar import monthrange

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
    
class StudentFirstSchedule(models.Model):
    year = models.IntegerField(validators=[MinValueValidator(2023), MaxValueValidator(9999)],default=2023)
    month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    student = models.ForeignKey(Student, on_delete=models.CASCADE)# 生徒番号(外部キー制約)
    
    def clean(self):
        # year, month, dayがすべて指定されているかチェック
        if self.year is not None and self.month is not None and self.day is not None:
            # monthrange関数は指定した月の日数を返す
            _, last_day = monthrange(self.year, self.month)
            # 指定した日がその月の日数を超えていないかチェック
            if self.day > last_day:
                raise ValidationError({
                    'day': ValidationError(
                        'この月は %(last_day)d日までです。',
                        code='invalid',
                        params={'last_day': last_day},
                    ),
                })
        super().clean()
    
class StudentSecondSchedule(models.Model):
    year = models.IntegerField(validators=[MinValueValidator(2023), MaxValueValidator(9999)],default=2023)
    month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    student = models.ForeignKey(Student, on_delete=models.CASCADE)# 生徒番号(外部キー制約)
    
    def clean(self):
        # year, month, dayがすべて指定されているかチェック
        if self.year is not None and self.month is not None and self.day is not None:
            # monthrange関数は指定した月の日数を返す
            _, last_day = monthrange(self.year, self.month)
            # 指定した日がその月の日数を超えていないかチェック
            if self.day > last_day:
                raise ValidationError({
                    'day': ValidationError(
                        'この月は %(last_day)d日までです。',
                        code='invalid',
                        params={'last_day': last_day},
                    ),
                })
        super().clean()

# class ShiftRequest(models.Model):
#     year = models.IntegerField()
#     month = models.IntegerField()
#     day = models.IntegerField()
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
#     is_avaliabe = models.BooleanField(default=False)
   
# class Shift(models.Model):
#     year = models.IntegerField()
#     month = models.IntegerField()
#     day = models.IntegerField()
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
#     student_first = models.ForeignKey(Student, on_delete=models.CASCADE,null=True,related_name='first_shifts')
#     student_second = models.ForeignKey(Student, on_delete=models.CASCADE,null=True,related_name='second_shifts')