from .models import *

def get_student_list(value_year, value_month, value_day):
    student_list_first = StudentFirstSchedule.objects.filter(year=value_year, month=value_month, day=value_day).values_list('student', flat=True)
    student_list_second = StudentSecondSchedule.objects.filter(year=value_year, month=value_month, day=value_day).values_list('student', flat=True)
    student_list = list(student_list_first) + list(student_list_second)
    return student_list

def get_student_teacher_list(year, month, day):
    student_list = get_student_list(year, month, day)
    student_teacher_list = Student.objects.filter(student_number__in=student_list).values_list('teacher', flat=True)
    return student_teacher_list

def get_teacher_list(value_year, value_month, value_day):
    teacher_list = list(TeacherSchedule.objects.filter(year=value_year, month=value_month, day=value_day).values_list('teacher', flat=True))
    return teacher_list


#辞書型で講師番号と生徒との一致回数を返す
def teacher_decision(year, month, day):
    student_teacher_list = get_student_teacher_list(year, month, day)
    teacher_list = get_teacher_list(year, month, day)
    # 回数を保持する辞書を初期化
    match_count_dict = {}
    for x in range(len(student_teacher_list)):
        for y in range(len(teacher_list)):
            if student_teacher_list[x] == teacher_list[y]:
                if student_teacher_list[x] in match_count_dict:
                    match_count_dict[student_teacher_list[x]] += 1
                else:
                    match_count_dict[student_teacher_list[x]] = 1
    return match_count_dict