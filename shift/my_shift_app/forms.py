from django import forms
from .models import Teacher, Student

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