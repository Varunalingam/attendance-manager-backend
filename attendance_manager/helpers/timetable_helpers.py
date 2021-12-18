

from attendance_manager.models import ClassRepresentative


def check_cr_permission_course(student,course):
    try:
        if course.section_id == None:
            ClassRepresentative.objects.get(student_id = student, rep_of_type=ClassRepresentative.RepType.Section, rep_of_id=course.section_id)
        else:
            ClassRepresentative.objects.get(student_id = student, rep_of_type=ClassRepresentative.RepType.Course, rep_of_id=course.course_id)
    except:
        return False
    return True

def check_cr_permission_section(student):
    try:
        ClassRepresentative.objects.get(student_id = student, rep_of_type=ClassRepresentative.RepType.Section, rep_of_id=student.section.section_id)
    except:
        return False
    return True