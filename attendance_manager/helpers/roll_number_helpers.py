from attendance_manager.models import Department, Section
from datetime import date


def getDepartmentFromRollNumber(rollnumber):
    department_names = {
        '110' : 'Instrumentation and Control Engineering',
        '101' : 'Architecture',
        '102' : 'Chemical Engineering',
        '103' : 'Civil Engineering',
        '106' : 'Computer Science and Engineering',
        '107' : 'Electrical and Electronics Engineering',
        '108' : 'Electronics and Communication Engineering',
        '111' : 'Mechanical Engineering',
        '112' : 'Metallurgical and Materials Engineering',
        '114' : 'Production Engineering'
    }
    return Department.objects.get(department_name=department_names[rollnumber[0:3]])

def getBatchFromRollNumber(rollnumber):
    return date(1900 + int(rollnumber[3:6]) + 4, 6, 1)

def getSectionFromRollNumber(rollnumber):
    single_section_departments = [
        'Metallurgical and Materials Engineering',
        'Chemical Engineering'
    ]
    department = getDepartmentFromRollNumber(rollnumber)
    if department.department_name in single_section_departments:
        return Section.objects.get(department = department.department_id)
    section_names = {
        'odd' : 'A',
        'even' : 'B'
    }
    section_type = int(rollnumber[6:9])
    batch = getBatchFromRollNumber(rollnumber)
    if (section_type % 2 == 0):
        return Section.objects.get(department = department.department_id, section_name = section_names['even'], batch=batch)
    else:
        return Section.objects.get(department = department.department_id, section_name = section_names['odd'], batch=batch)

