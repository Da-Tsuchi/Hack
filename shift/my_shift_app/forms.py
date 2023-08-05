from django import forms
from .models import *

# 年月を選択するフォーム
class MonthYearForm(forms.Form):
    YEARS = [(year, year) for year in range(2023, 2100)]
    MONTHS = [(month, month) for month in range(1, 13)]
    year = forms.ChoiceField(choices=YEARS)
    month = forms.ChoiceField(choices=MONTHS)
    
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['teacher_number', 'name']  # フォームにteacher_numberフィールドを追加

class StudentForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all(), to_field_name="teacher_number")
    class Meta:
        model = Student
        fields = ['student_number', 'name', 'teacher']
        
    def clean_teacher(self):
        teacher = self.cleaned_data.get('teacher')
        if not Teacher.objects.filter(teacher_number=teacher.teacher_number).exists():
            raise forms.ValidationError("Selected teacher does not exist.")
        return teacher
    
class StudentFirstScheduleForm(forms.ModelForm):
    year = forms.IntegerField()
    month = forms.IntegerField()
    day = forms.IntegerField()
    student = forms.ModelChoiceField(queryset=Student.objects.all())
    
    class Meta:
        model = StudentFirstSchedule
        fields = ['year', 'month',"day","student"]  # フォームにteacher_numberフィールドを追加
        
class StudentSecondScheduleForm(forms.ModelForm):
    year = forms.IntegerField()
    month = forms.IntegerField()
    day = forms.IntegerField()
    student = forms.ModelChoiceField(queryset=Student.objects.all())
    
    class Meta:
        model = StudentFirstSchedule
        fields = ['year', 'month',"day","student"]  # フォームにteacher_numberフィールドを追加

class ShiftForm(forms.Form):
    day = forms.IntegerField()
    student_first = forms.ChoiceField(widget=forms.Select)
    student_second = forms.ChoiceField(widget=forms.Select)

    def __init__(self, *args, **kwargs):
        shifts_first = kwargs.pop('shifts_first')
        shifts_second = kwargs.pop('shifts_second')
        super(ShiftForm, self).__init__(*args, **kwargs)

        self.fields['student_first'].choices = [(shift.student_first.id, shift.student_first.name) for shift in shifts_first]
        self.fields['student_second'].choices = [(shift.student_second.id, shift.student_second.name) for shift in shifts_second]