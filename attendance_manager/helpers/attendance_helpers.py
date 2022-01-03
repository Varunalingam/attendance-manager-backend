from attendance_manager.models import Attendance, TimeTable

def generate_attendance(student, course_id):
    timetables = TimeTable.objects.filter(course_id = course_id).values_list("timetable_id", flat=True)
    for timetable_id in timetables:
        timetable = TimeTable.objects.get(timetable_id = timetable_id)
        Attendance.objects.get_or_create(timetable_id=timetable, student_id = student)
