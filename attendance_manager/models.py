from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.TextField(max_length=2000, null=False)

class Section(models.Model):
    section_id = models.AutoField(primary_key=True)
    department = models.ForeignKey(Department, db_column='department_id', on_delete=models.CASCADE)
    section_name = models.TextField(max_length=2)
    batch = models.DateField(null=False)

from attendance_manager.helpers.roll_number_helpers import getBatchFromRollNumber, getDepartmentFromRollNumber, getSectionFromRollNumber
    
class Courses(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.TextField(max_length=2000, null=False)
    course_code = models.TextField(max_length=6, null=False)
    
    class CoursePeriod(models.TextChoices):
        Summer = 'Summer', ('Summer')
        Winter = 'Winter', ('Winter')
    
    course_period = models.CharField(max_length=8, choices=CoursePeriod.choices, default=CoursePeriod.Summer)
    course_year = models.DateField(null=False)

    section_id = models.ForeignKey(Section, db_column='section_id', on_delete=models.DO_NOTHING, null=True, blank=True)
    department_id = models.ForeignKey(Department, db_column='department_id', on_delete=models.CASCADE)

    class CourseType(models.TextChoices):
        Program_Core = 'PC', ('Program Core')
        Program_Elective = 'PE', ('Program Elective')
        Open_Elective = 'OE', ('Open Elective')
        Minors = 'M', ('Minors')
        Institute_Requirement = 'IR', ('Institute Requirement')
        Labratory_Requirement = 'LR', ('Labratory Requirement')

    course_type = models.CharField(max_length=4, choices=CourseType.choices, default=CourseType.Program_Core)
    no_of_classes = models.IntegerField()
    credits = models.IntegerField()
    minimum_attendance_percentage = models.FloatField(default=0.75)

class UserManager(BaseUserManager):
    def create_user(self, roll_no, password=" "):
        """
        Creates and saves a User with the given roll_no and password.
        """
        if not roll_no:
            raise ValueError('Users must have an roll_no address')

        user = self.model(
            roll_no=roll_no
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, roll_no, password = " "):
        """
        Creates and saves a superuser with the given roll_no and password.
        """
        user = self.create_user(
            roll_no=roll_no,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class Student(AbstractBaseUser):
    student_id = models.AutoField(primary_key=True)
    username = None
    roll_no = models.CharField(max_length=9, null=False, unique=True)
    name = models.TextField(max_length=2000, null=True)
    department_id = models.ForeignKey(Department, db_column='department_id', on_delete=models.DO_NOTHING)
    section_id = models.ForeignKey(Section, db_column='section_id', on_delete=models.DO_NOTHING)
    batch = models.DateField()
    otp = models.TextField(max_length=6, null= True)
    otp_timeout = models.DateTimeField(null= True)
    def save(self, *args, **kwargs):
        self.department_id = getDepartmentFromRollNumber(self.roll_no)
        self.section_id = getSectionFromRollNumber(self.roll_no)
        self.batch = getBatchFromRollNumber(self.roll_no)
        super(Student, self).save(*args, **kwargs)

    objects = UserManager()

    USERNAME_FIELD = 'roll_no'
    REQUIRED_FIELDS = []
    
    def get_full_name(self):
        # The user is identified by their email address
        return self.roll_no + '@nitt.edu'

    def get_short_name(self):
        # The user is identified by their email address
        return self.roll_no

    def __str__(self):
        return self.roll_no

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return self.roll_no == '110119123'

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.roll_no == '110119123'

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.roll_no == '110119123'

class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    title = models.TextField(max_length=2000, null=False)
    message = models.TextField(max_length=2000, null=True)
    date_of_sending = models.DateTimeField()
    file_link = models.TextField(null=True)
    receiver_id = models.IntegerField()
    class ReceiverType(models.TextChoices):
        Department = 'D', ('Department')
        Course = 'C', ('Course')
        Section = 'S', ('Section')
    receiver_type = models.TextField(max_length=2, choices=ReceiverType.choices, default=ReceiverType.Course)

class TimeTable(models.Model):
    timetable_id = models.AutoField(primary_key=True)
    starttime = models.DateTimeField(null=False)
    endtime = models.DateTimeField(null=False)
    course_id = models.ForeignKey(Courses, db_column='course_id', on_delete=models.CASCADE)
    class Status(models.TextChoices):
        Suspended = 'S', ('Suspended')
        Modified = 'M', ('Modified')
        Active = 'A', ('Active')
    status = models.TextField(max_length=2, choices=Status.choices, default=Status.Active)

class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, db_column='student_id', on_delete=models.CASCADE)
    timetable_id = models.ForeignKey(TimeTable, db_column='timetable_id', on_delete=models.CASCADE)
    present_status = models.BooleanField(default=False)

class ClassRepresentative(models.Model):
    class_rep_id = models.AutoField(primary_key=True)
    rep_of_id = models.IntegerField()
    class RepType(models.TextChoices):
        Course = 'C', ('Course')
        Section = 'S', ('Section')
    rep_of_type = models.TextField(max_length=2, choices=RepType.choices, default=RepType.Course)
    student_id = models.ForeignKey(Student, db_column='student_id', on_delete=models.CASCADE)

class CourseStudents(models.Model):
    course_student_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, db_column='student_id', on_delete=models.CASCADE)
    course_id = models.ForeignKey(Courses, db_column='course_id', on_delete=models.CASCADE)

    
