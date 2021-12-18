
from attendance_manager.models import CourseStudents, Courses, Section
from django.utils import timezone

def get_courses(student):
    course_period = Courses.CoursePeriod.Winter
    if timezone.now().month < 6:
        course_period = Courses.CoursePeriod.Summer  
    course_year = timezone.now().date()
    course_year = course_year.replace(day=1, month=6)
    courses = CourseStudents.objects.filter(student_id=student, course_id__course_period=course_period, course_id__course_year=course_year).values_list('course_id',flat=True)
    courses = Courses.objects.filter(pk__in=courses)
    print(courses)
    print(student.section_id)
    print(Courses.objects.all())
    print(course_period)
    print(Courses.objects.filter(section_id=student.section_id, course_period=course_period, course_year=course_year))
    courses = courses.union(Courses.objects.filter(section_id=student.section_id, course_period=course_period, course_year=course_year))
    return courses

def get_all_elective(student):
    course_period = Courses.CoursePeriod.Winter
    if timezone.now().month < 6:
        course_period = Courses.CoursePeriod.Summer  
    course_year = timezone.now().date()
    course_year = course_year.replace(day=1, month=6)
    courses = Courses.objects.filter(course_year = course_year, course_period=course_period, section_id=None).exclude(course_type__in=[Courses.CourseType.Institute_Requirement, Courses.CourseType.Labratory_Requirement, Courses.CourseType.Program_Core])
    courses = courses.filter(course_type=Courses.CourseType.Program_Elective, department_id=student.department_id).union(courses.exclude(course_type=Courses.CourseType.Program_Elective).exclude(department_id=student.department_id))
    return courses