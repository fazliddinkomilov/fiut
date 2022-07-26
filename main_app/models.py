from datetime import datetime, timezone
from fnmatch import translate

from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Length
from django.db.models import TextField, Q
from django.utils.translation import gettext as _

TextField.register_lookup(Length, 'length')


class News(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=500)
    description = models.TextField(verbose_name=_('Description'))
    image = models.ImageField(verbose_name=_('Image'), null=False, blank=False)
    registrationlink = models.URLField(verbose_name=_('RegistrationLink'), null=True, blank=True)

    class Meta:

        verbose_name = _('New')
        verbose_name_plural = _('News')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cleaned_data = None

    def __str__(self):
        return self.title

    def is_valid(self):
        pass


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)


class Session(models.Model):
    start_year = models.DateField(verbose_name=_('start_year'))
    end_year = models.DateField(verbose_name=_('end_year'))

    def __str__(self):
        return "From " + str(self.start_year) + " to " + str(self.end_year)


class CustomUser(AbstractUser):
    USER_TYPE = ((1, "HOD"), (2, "Staff"), (3, "Student"), (4, "HR"))
    GENDER = [("M", "Male"), ("F", "Female")]

    username = None  # Removed username, using email instead
    email = models.EmailField(verbose_name=_('email'), unique=True)
    user_type = models.CharField(verbose_name=_('user_type'), default=1, choices=USER_TYPE, max_length=1)
    gender = models.CharField(verbose_name=_('gender'), max_length=1, choices=GENDER)
    profile_pic = models.ImageField(verbose_name=_('profile_pic'))
    address = models.TextField(verbose_name=_('address'))
    fcm_token = models.TextField(verbose_name=_('fcm_token'), default="")  # For firebase notifications
    created_at = models.DateTimeField(verbose_name=_('created_at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated_at'), auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.last_name + ", " + self.first_name


class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class Course(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=120)
    created_at = models.DateTimeField(verbose_name=_('created_at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated_at'), auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cleaned_data = None

    def __str__(self):
        return self.name

    def is_valid(self):
        pass


class Student(models.Model):
    MARRIED = [("M", _("Married")), ("N", _("Not Married"))]
    PAY_TYPE = [("C", _("Contract")), ("B", _("Budget"))]
    COURSE_NUMBER = [("1", _("1-course")), ("2", _("2-course")), ("3", _("3-course"))]
    LOCATION_TYPE = [("1", _("I live in my house")), ("2", _("I live in a communal apartment")), ("3", _("I live in a hotel"))]

    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course,verbose_name=_('course'), on_delete=models.DO_NOTHING, null=True, blank=False)
    session = models.ForeignKey(Session,verbose_name=_('session'), on_delete=models.DO_NOTHING, null=True)
    date_of_birth = models.DateField(verbose_name=_('date_of_birth'),null=True)
    phone_number = PhoneNumberField(verbose_name=_('phone_number'),null=True, blank=True)
    home_number = PhoneNumberField(verbose_name=_('home_number'),null=True, blank=True)
    nationality = models.CharField(verbose_name=_('nationality'),max_length=120, null=True, blank=True)
    marital_status = models.CharField(verbose_name=_('marital_status'),null=True, max_length=1, choices=MARRIED, blank=True)
    education_pay_type = models.CharField(verbose_name=_('education_pay_type'),null=True, max_length=1, choices=PAY_TYPE, blank=True)
    course_level = models.CharField(verbose_name=_('course_level'),null=True, max_length=1, choices=COURSE_NUMBER, blank=True)
    location_type_name = models.CharField(verbose_name=_('location_type_name'),null=True, max_length=1, choices=LOCATION_TYPE, blank=True)
    admission_date = models.DateField(verbose_name=_('admission_date'),null=True, blank=True)
    ITN = models.CharField(verbose_name=_('ITN'),null=True, max_length=50, blank=True)
    passport_picture_front = models.ImageField(verbose_name=_('passport_picture_front'),null=True, blank=True)
    passport_picture_back = models.ImageField(verbose_name=_('passport_picture_back'),null=True, blank=True)

    def __str__(self):
        return self.admin.last_name + ", " + self.admin.first_name


class Staff(models.Model):
    MARRIED = [("M", _("Married")), ("N", _("Not Married"))]
    PAY_TYPE = [("C", _("Contract")), ("B", _("Budget"))]
    COURSE_NUMBER = [("1", _("1-course")), ("2", _("2-course")), ("3", _("3-course"))]
    LOCATION_TYPE = [("1", _("I live in my house")), ("2", _("I live in a communal apartment")), ("3", _("I live in a hotel"))]

    course = models.ForeignKey(Course, verbose_name=_('course'), on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField(verbose_name=_('date_of_birth'),null=True)
    phone_number = PhoneNumberField(verbose_name=_('phone_number'),null=True, blank=True)
    home_number = PhoneNumberField(verbose_name=_('home_number'),null=True, blank=True)
    nationality = models.CharField(verbose_name=_('nationality'),max_length=120, null=True)
    marital_status = models.CharField(verbose_name=_('marital_status'),null=True, max_length=1, choices=MARRIED)
    location_type_name = models.CharField(verbose_name=_('location_type_name'),null=True, max_length=1, choices=LOCATION_TYPE)
    ITN = models.CharField(verbose_name=_('ITN'),null=True, max_length=50, blank=True)
    passport_picture_front = models.ImageField(verbose_name=_('passport_picture_front'),null=True, blank=True)
    passport_picture_back = models.ImageField(verbose_name=_('passport_picture_back'),null=True, blank=True)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name


class HR(models.Model):
    MARRIED = [("M", _("Married")), ("N", _("Not Married"))]
    PAY_TYPE = [("C", _("Contract")), ("B", _("Budget"))]
    COURSE_NUMBER = [("1", _("1-course")), ("2", _("2-course")), ("3", _("3-course"))]
    LOCATION_TYPE = [("1", _("I live in my house")), ("2", _("I live in a communal apartment")), ("3", _("I live in a hotel"))]

    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField(verbose_name=_('date_of_birth'),null=True)
    phone_number = PhoneNumberField(verbose_name=_('phone_number'),null=True, blank=True)
    home_number = PhoneNumberField(verbose_name=_('home_number'),null=True, blank=True)
    nationality = models.CharField(verbose_name=_('nationality'),max_length=120, null=True)
    marital_status = models.CharField(verbose_name=_('marital_status'),null=True, max_length=1, choices=MARRIED)
    location_type_name = models.CharField(verbose_name=_('location_type_name'),null=True, max_length=1, choices=LOCATION_TYPE, blank=True)
    ITN = models.CharField(verbose_name=_('ITN'),null=True, max_length=50, blank=True)
    passport_picture_front = models.ImageField(verbose_name=_('passport_picture_front'),null=True, blank=True)
    passport_picture_back = models.ImageField(verbose_name=_('passport_picture_back'),null=True, blank=True)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name


class Subject(models.Model):
    name = models.CharField(verbose_name=_('name'),max_length=120)
    staff = models.ForeignKey(Staff,verbose_name=_('staff'), on_delete=models.CASCADE)
    course = models.ForeignKey(Course,verbose_name=_('course'), on_delete=models.CASCADE)
    updated_at = models.DateTimeField(verbose_name=_('updated_at'),auto_now=True)
    created_at = models.DateTimeField(verbose_name=_('created_at'),auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cleaned_data = None

    def __str__(self):
        return self.name

    def is_valid(self):
        pass


class Attendance(models.Model):
    session = models.ForeignKey(Session,verbose_name=_('session'), on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject,verbose_name=_('subject'), on_delete=models.DO_NOTHING)
    date = models.DateField(verbose_name=_('date'))
    created_at = models.DateTimeField(verbose_name=_('created_at'),auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated_at'),auto_now=True)


class AttendanceReport(models.Model):
    student = models.ForeignKey(Student, verbose_name=_('student'), on_delete=models.DO_NOTHING)
    attendance = models.ForeignKey(Attendance, verbose_name=_('attendance'), on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.CharField(verbose_name=_('date'),max_length=60)
    message = models.TextField(verbose_name=_('message'),)
    status = models.SmallIntegerField(verbose_name=_('status'),default=0)
    created_at = models.DateTimeField(verbose_name=_('created_at'),auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated_at'),auto_now=True)


class LeaveReportStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.CharField(verbose_name=_('date'),max_length=60)
    message = models.TextField(verbose_name=_('message'))
    status = models.SmallIntegerField(verbose_name=_('status'),default=0)
    created_at = models.DateTimeField(verbose_name=_('created_at'),auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated_at'),auto_now=True)


class LeaveReportHR(models.Model):
    hr = models.ForeignKey(HR, on_delete=models.CASCADE)
    date = models.CharField(verbose_name=_('date'),max_length=60)
    message = models.TextField(verbose_name=_('message'))
    status = models.SmallIntegerField(verbose_name=_('status'),default=0)
    created_at = models.DateTimeField(verbose_name=_('created_at'),auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated_at'),auto_now=True)


class FeedbackStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField(verbose_name=_('feedback'))
    reply = models.TextField(verbose_name=_('reply'))
    created_at = models.DateTimeField(verbose_name=_('created_at'),auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated_at'),auto_now=True)


class FeedbackStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.TextField(verbose_name=_('feedback'),)
    reply = models.TextField(verbose_name=_('reply'))
    created_at = models.DateTimeField(verbose_name=_('created_at'),auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated_at'),auto_now=True)


class FeedbackHR(models.Model):
    hr = models.ForeignKey(HR, on_delete=models.CASCADE)
    feedback = models.TextField(verbose_name=_('feedback'))
    reply = models.TextField(verbose_name=_('reply'))
    created_at = models.DateTimeField(verbose_name=_('created_at'),auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated_at'),auto_now=True)


class NotificationStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField(verbose_name=_('message'))
    created_at = models.DateTimeField(verbose_name=_('created_at'),auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated_at'),auto_now=True)


class NotificationHR(models.Model):
    hr = models.ForeignKey(HR, on_delete=models.CASCADE)
    feedback = models.TextField(verbose_name=_('feedback'))
    reply = models.TextField(verbose_name=_('reply'),)
    created_at = models.DateTimeField(verbose_name=_('created_at'),auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated_at'),auto_now=True)


class NotificationStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField(verbose_name=_('message'),)
    created_at = models.DateTimeField(verbose_name=_('created_at'),auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated_at'),auto_now=True)


class StudentResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test = models.FloatField(verbose_name=_('test'),default=0)
    exam = models.FloatField(verbose_name=_('exam'),default=0)
    created_at = models.DateTimeField(verbose_name=_('created_at'),auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated_at'),auto_now=True)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Staff.objects.create(admin=instance)
        if instance.user_type == 3:
            Student.objects.create(admin=instance)
        if instance.user_type == 4:
            HR.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.student.save()
    if instance.user_type == 4:
        instance.hr.save()
