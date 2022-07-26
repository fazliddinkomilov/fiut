import json
import requests
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from .forms import *
from .models import *

from django.utils.translation import gettext as _


def admin_news(request):
    news = News.objects.all().order_by('-id')
    total_staff = Staff.objects.all().count()
    total_students = Student.objects.all().count()
    subjects = Subject.objects.all()
    total_subject = subjects.count()
    total_course = Course.objects.all().count()
    attendance_list = Attendance.objects.filter(subject__in=subjects)
    total_attendance = attendance_list.count()
    attendance_list = []
    subject_list = []
    for subject in subjects:
        attendance_count = Attendance.objects.filter(subject=subject).count()
        subject_list.append(subject.name[:7])
        attendance_list.append(attendance_count)
    context = {
        'page_title': _("Administrative Dashboard"),
        'total_students': total_students,
        'total_staff': total_staff,
        'total_course': total_course,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'news': news,
        'attendance_list': attendance_list

    }
    return render(request, 'hod_template/admin_news.html', context)


def admin_home(request):
    total_staff = Staff.objects.all().count()
    total_students = Student.objects.all().count()
    subjects = Subject.objects.all()
    total_subject = subjects.count()
    total_course = Course.objects.all().count()
    attendance_list = Attendance.objects.filter(subject__in=subjects)
    total_attendance = attendance_list.count()
    attendance_list = []
    subject_list = []
    for subject in subjects:
        attendance_count = Attendance.objects.filter(subject=subject).count()
        subject_list.append(subject.name[:7])
        attendance_list.append(attendance_count)
    context = {
        'page_title': _("Analytics"),
        'page_title2': _("Statistical Pie"),
        'total_students': total_students,
        'total_staff': total_staff,
        'total_course': total_course,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list

    }
    return render(request, 'hod_template/home_content.html', context)


def add_news(request):
    form = NewsForm(request.POST or None, request.FILES or None)
    context = {'form': form, 'page_title': _('Add New')}
    if request.method == 'POST':
        if form.is_valid():
            title = form.cleaned_data.get('title')
            title_en = form.cleaned_data.get('title_en')
            title_ru = form.cleaned_data.get('title_ru')
            title_uz = form.cleaned_data.get('title_uz')
            description = form.cleaned_data.get('description')
            description_en = form.cleaned_data.get('description_en')
            description_ru = form.cleaned_data.get('description_ru')
            description_uz = form.cleaned_data.get('description_uz')
            image = request.FILES.get('image')
            registrationlink = form.cleaned_data.get('registrationlink')
            try:
                news = News.objects.create(
                    title=title, description=description, registrationlink=registrationlink, image=image)
                news.title = title
                news.title_en = title_en
                news.title_ru = title_ru
                news.title_uz = title_uz
                news.description = description
                news.description_ru = description_ru
                news.description_en = description_en
                news.description_uz = description_uz
                news.registrationlink = registrationlink
                news.image = image
                news.save()
                messages.success(request, _("Successfully Added"))
                return redirect(reverse('admin_news'))

            except Exception as e:
                messages.error(request, _("Could Not Add ") + str(e))

        else:
            messages.error(request, _("Please fulfil all requirements"))

    return render(request, 'hod_template/add_news_template.html', context)


def add_staff(request):
    form = StaffForm(request.POST or None, request.FILES or None)
    context = {'form': form, 'page_title': _('Add Staff')}
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password')
            course = form.cleaned_data.get('course')

            date_of_birth = form.cleaned_data.get('date_of_birth')
            phone_number = form.cleaned_data.get('phone_number')
            home_number = form.cleaned_data.get('home_number')
            nationality = form.cleaned_data.get('nationality')
            marital_status = form.cleaned_data.get('marital_status')
            education_pay_type = form.cleaned_data.get('education_pay_type')
            location_type_name = form.cleaned_data.get('location_type_name')
            admission_date = form.cleaned_data.get('admission_date')
            ITN = form.cleaned_data.get('ITN')
            passport_picture_front = form.cleaned_data.get('passport_picture_front')
            passport_picture_back = form.cleaned_data.get('passport_picture_back')

            passport = request.FILES.get('profile_pic')
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=2, first_name=first_name, last_name=last_name,
                    profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.staff.course = course

                user.staff.date_of_birth = date_of_birth
                user.staff.phone_number = phone_number
                user.staff.home_number = home_number
                user.staff.nationality = nationality
                user.staff.marital_status = marital_status
                user.staff.education_pay_type = education_pay_type
                user.staff.location_type_name = location_type_name
                user.staff.admission_date = admission_date
                user.staff.ITN = ITN
                user.staff.passport_picture_front = passport_picture_front
                user.staff.passport_picture_back = passport_picture_back

                user.save()
                messages.success(request, _("Successfully Added"))
                return redirect(reverse('add_staff'))

            except Exception as e:
                messages.error(request, _("Could Not Add ") + str(e))
        else:
            messages.error(request, _("Please fulfil all requirements"))

    return render(request, 'hod_template/add_staff_template.html', context)


def add_hr(request):
    form = HRForm(request.POST or None, request.FILES or None)
    context = {'form': form, 'page_title': _('Add HR')}
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password')

            date_of_birth = form.cleaned_data.get('date_of_birth')
            phone_number = form.cleaned_data.get('phone_number')
            home_number = form.cleaned_data.get('home_number')
            nationality = form.cleaned_data.get('nationality')
            marital_status = form.cleaned_data.get('marital_status')
            education_pay_type = form.cleaned_data.get('education_pay_type')
            location_type_name = form.cleaned_data.get('location_type_name')
            admission_date = form.cleaned_data.get('admission_date')
            ITN = form.cleaned_data.get('ITN')
            passport_picture_front = form.cleaned_data.get('passport_picture_front')
            passport_picture_back = form.cleaned_data.get('passport_picture_back')

            passport = request.FILES.get('profile_pic')
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=4, first_name=first_name, last_name=last_name,
                    profile_pic=passport_url)
                user.gender = gender
                user.address = address

                user.hr.date_of_birth = date_of_birth
                user.hr.phone_number = phone_number
                user.hr.home_number = home_number
                user.hr.nationality = nationality
                user.hr.marital_status = marital_status
                user.hr.education_pay_type = education_pay_type
                user.hr.location_type_name = location_type_name
                user.hr.admission_date = admission_date
                user.hr.ITN = ITN
                user.hr.passport_picture_front = passport_picture_front
                user.hr.passport_picture_back = passport_picture_back

                user.save()
                messages.success(request, _("Successfully Added"))
                return redirect(reverse('add_hr'))

            except Exception as e:
                messages.error(request, _("Could Not Add ") + str(e))
        else:
            messages.error(request, _("Please fulfil all requirements"))

    return render(request, 'hod_template/add_hr_template.html', context)


def add_student(request):
    student_form = StudentForm(request.POST or None, request.FILES or None)
    context = {'form': student_form, 'page_title': _('Add Student')}
    if request.method == 'POST':
        if student_form.is_valid():
            first_name = student_form.cleaned_data.get('first_name')
            last_name = student_form.cleaned_data.get('last_name')
            address = student_form.cleaned_data.get('address')
            email = student_form.cleaned_data.get('email')
            gender = student_form.cleaned_data.get('gender')
            password = student_form.cleaned_data.get('password')
            course = student_form.cleaned_data.get('course')
            session = student_form.cleaned_data.get('session')

            date_of_birth = student_form.cleaned_data.get('date_of_birth')
            phone_number = student_form.cleaned_data.get('phone_number')
            home_number = student_form.cleaned_data.get('home_number')
            nationality = student_form.cleaned_data.get('nationality')
            marital_status = student_form.cleaned_data.get('marital_status')
            education_pay_type = student_form.cleaned_data.get('education_pay_type')
            course_level = student_form.cleaned_data.get('course_level')
            location_type_name = student_form.cleaned_data.get('location_type_name')
            admission_date = student_form.cleaned_data.get('admission_date')
            ITN = student_form.cleaned_data.get('ITN')
            passport_picture_front = student_form.cleaned_data.get('passport_picture_front')
            passport_picture_back = student_form.cleaned_data.get('passport_picture_back')

            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=3, first_name=first_name, last_name=last_name,
                    profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.student.session = session
                user.student.course = course
                user.student.date_of_birth = date_of_birth
                user.student.phone_number = phone_number
                user.student.home_number = home_number
                user.student.nationality = nationality
                user.student.marital_status = marital_status
                user.student.education_pay_type = education_pay_type
                user.student.course_level = course_level
                user.student.location_type_name = location_type_name
                user.student.admission_date = admission_date
                user.student.ITN = ITN
                user.student.passport_picture_front = passport_picture_front
                user.student.passport_picture_back = passport_picture_back
                user.save()
                messages.success(request, _("Successfully Added"))
                return redirect(reverse('add_student'))
            except Exception as e:
                messages.error(request, _("Could Not Add: ") + str(e))
        else:
            messages.error(request, _("Could Not Add: "))
    return render(request, 'hod_template/add_student_template.html', context)


def add_course(request):
    form = CourseForm(request.POST or None)
    context = {
        'form': form,
        'page_title': _('Add Course')
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            name_en = form.cleaned_data.get('name_en')
            name_ru = form.cleaned_data.get('name_ru')
            try:
                course = Course()
                course.name = name
                course.name_en = name_en
                course.name_ru = name_ru
                course.save()
                messages.success(request, _("Successfully Added"))
                return redirect(reverse('add_course'))
            except:
                messages.error(request, _("Could Not Add"))
        else:
            messages.error(request, _("Could Not Add"))
    return render(request, 'hod_template/add_course_template.html', context)


def add_subject(request):
    form = SubjectForm(request.POST or None)
    context = {
        'form': form,
        'page_title': _('Add Subject')
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            name_en = form.cleaned_data.get('name_en')
            name_ru = form.cleaned_data.get('name_ru')
            name_uz = form.cleaned_data.get('name_ru')
            course = form.cleaned_data.get('course')
            staff = form.cleaned_data.get('staff')
            try:
                subject = Subject.objects.create(name=name, staff=staff, course=course)
                subject.name = name
                subject.name_en = name_en
                subject.name_ru = name_ru
                subject.name_uz = name_uz

                subject.staff = staff
                subject.course = course
                subject.save()
                messages.success(request, _("Successfully Added"))
                return redirect(reverse('manage_subject'))

            except Exception as e:
                messages.error(request, _("Could Not Add ") + str(e))
        else:
            messages.error(request, _("Fill Form Properly"))

    return render(request, 'hod_template/add_subject_template.html', context)


def manage_staff(request):
    allStaff = CustomUser.objects.filter(user_type=2)
    context = {
        'allStaff': allStaff,
        'page_title': _('Manage Staff'),
    }
    return render(request, "hod_template/manage_staff.html", context)


def manage_hr(request):
    allHR = CustomUser.objects.filter(user_type=4)
    context = {
        'allHR': allHR,
        'page_title': _('Manage HR'),
    }
    return render(request, "hod_template/manage_hr.html", context)


def manage_student(request):
    students = CustomUser.objects.filter(user_type=3)
    context = {
        'students': students,
        'page_title': _('Manage Students'),
    }
    return render(request, "hod_template/manage_student.html", context)


def manage_course(request):
    courses = Course.objects.all()
    context = {
        'courses': courses,
        'page_title': _('Manage Courses'),
    }
    return render(request, "hod_template/manage_course.html", context)


def manage_subject(request):
    subjects = Subject.objects.all()
    context = {
        'subjects': subjects,
        'page_title': _('Manage Subjects'),
    }
    return render(request, "hod_template/manage_subject.html", context)


def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    form = StaffForm(request.POST or None, instance=staff)
    context = {
        'form': form,
        'staff_id': staff_id,
        'page_title': _('Edit Staff'),
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            course = form.cleaned_data.get('course')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=staff.admin.id)
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.first_name = first_name
                user.last_name = last_name
                user.gender = gender
                user.address = address
                staff.course = course
                user.save()
                staff.save()
                messages.success(request, _("Successfully Updated"))
                return redirect(reverse('edit_staff', args=[staff_id]))
            except Exception as e:
                messages.error(request, _("Could Not Update ") + str(e))
        else:
            messages.error(request, _("Please fil form properly"))
    else:
        user = CustomUser.objects.get(id=staff_id)
        staff = Staff.objects.get(id=user.id)
        return render(request, "hod_template/edit_staff_template.html", context)


def edit_hr(request, hr_id):
    hr = get_object_or_404(HR, id=hr_id)
    form = HRForm(request.POST or None, instance=hr)
    context = {
        'form': form,
        'hr_id': hr_id,
        'page_title': _('Edit HR')
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            course = form.cleaned_data.get('course')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=hr.admin.id)
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.first_name = first_name
                user.last_name = last_name
                user.gender = gender
                user.address = address
                hr.course = course
                user.save()
                hr.save()
                messages.success(request, _("Successfully Updated"))
                return redirect(reverse('edit_hr', args=[hr_id]))
            except Exception as e:
                messages.error(request, _("Could Not Update ") + str(e))
        else:
            messages.error(request, _("Please fil form properly"))
    else:
        user = CustomUser.objects.get(id=hr_id)
        hr = HR.objects.get(id=user.id)
        return render(request, "hod_template/edit_staff_template.html", context)


def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    form = StudentForm(request.POST or None, instance=student)
    context = {
        'form': form,
        'student_id': student_id,
        'page_title': _('Edit Student')
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            course = form.cleaned_data.get('course')
            session = form.cleaned_data.get('session')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=student.admin.id)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                student.session = session
                user.gender = gender
                user.address = address
                student.course = course
                user.save()
                student.save()
                messages.success(request, _("Successfully Updated"))
                return redirect(reverse('edit_student', args=[student_id]))
            except Exception as e:
                messages.error(request, _("Could Not Update ") + str(e))
        else:
            messages.error(request, _("Please Fill Form Properly!"))
    else:
        return render(request, "hod_template/edit_student_template.html", context)


def edit_course(request, course_id):
    instance = get_object_or_404(Course, id=course_id)
    form = CourseForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'course_id': course_id,
        'page_title': _('Edit Course')
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            name_en = form.cleaned_data.get('name_en')
            name_ru = form.cleaned_data.get('name_ru')
            try:
                course = Course.objects.get(id=course_id)
                course.name = name
                course.name_en = name_en
                course.name_ru = name_ru
                course.save()
                messages.success(request, _("Successfully Updated"))
            except:
                messages.error(request, _("Could Not Update"))
        else:
            messages.error(request, _("Could Not Update"))

    return render(request, 'hod_template/edit_course_template.html', context)


def edit_subject(request, subject_id):
    instance = get_object_or_404(Subject, id=subject_id)
    form = SubjectForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'subject_id': subject_id,
        'page_title': _('Edit Subject')
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            name_en = form.cleaned_data.get('name_en')
            name_ru = form.cleaned_data.get('name_ru')
            course = form.cleaned_data.get('course')
            staff = form.cleaned_data.get('staff')
            try:
                subject = Subject.objects.get(id=subject_id)
                subject.name = name
                subject.name_en = name_en
                subject.name_ru = name_ru
                subject.staff = staff
                subject.course = course
                subject.save()
                messages.success(request, _("Successfully Updated"))
                return redirect(reverse('edit_subject', args=[subject_id]))
            except Exception as e:
                messages.error(request, _("Could Not Add ") + str(e))
        else:
            messages.error(request, _("Fill Form Properly"))
    return render(request, 'hod_template/edit_subject_template.html', context)


def add_session(request):
    form = SessionForm(request.POST or None)
    context = {'form': form, 'page_title': _('Add Session')}
    if request.method == 'POST':
        if form.is_valid():
            start_year = form.cleaned_data.get('start_year')
            end_year = form.cleaned_data.get('end_year')
            try:
                form = Session.objects.create(
                    start_year=start_year, end_year=end_year)
                form.start_year = start_year
                form.end_year = end_year

                form.save()
                messages.success(request, _("Session Created"))
                return redirect(reverse('add_session'))
            except Exception as e:
                messages.error(request, _('Could Not Add ') + str(e))
        else:
            messages.error(request, _('Fill Form Properly '))
    return render(request, "hod_template/add_session_template.html", context)


def manage_session(request):
    sessions = Session.objects.all()
    context = {'sessions': sessions, 'page_title': _('Manage Sessions')}
    return render(request, "hod_template/manage_session.html", context)


def edit_session(request, session_id):
    instance = get_object_or_404(Session, id=session_id)
    form = SessionForm(request.POST or None, instance=instance)
    context = {'form': form, 'session_id': session_id,
               'page_title': _('Edit Session')}
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _("Session Updated"))
                return redirect(reverse('edit_session', args=[session_id]))
            except Exception as e:
                messages.error(
                    request, _("Session Could Not Be Updated ") + str(e))
                return render(request, "hod_template/edit_session_template.html", context)
        else:
            messages.error(request, _("Invalid Form Submitted "))
            return render(request, "hod_template/edit_session_template.html", context)

    else:
        return render(request, "hod_template/edit_session_template.html", context)


@csrf_exempt
def check_email_availability(request):
    email = request.POST.get("email")
    try:
        user = CustomUser.objects.filter(email=email).exists()
        if user:
            return HttpResponse(True)
        return HttpResponse(False)
    except Exception as e:
        return HttpResponse(False)


@csrf_exempt
def student_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackStudent.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': _('Student Feedback Messages')
        }
        return render(request, 'hod_template/student_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackStudent, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def staff_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackStaff.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': _('Staff Feedback Messages'),
        }
        return render(request, 'hod_template/staff_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackStaff, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def view_staff_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportStaff.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': _('Leave Applications From Staff'),
        }
        return render(request, "hod_template/staff_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportStaff, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


@csrf_exempt
def view_student_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportStudent.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': _('Leave Applications From Students'),
        }
        return render(request, "hod_template/student_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportStudent, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


def admin_view_attendance(request):
    subjects = Subject.objects.all()
    sessions = Session.objects.all()
    context = {
        'subjects': subjects,
        'sessions': sessions,
        'page_title': _('View Attendance'),
    }

    return render(request, "hod_template/admin_view_attendance.html", context)


@csrf_exempt
def get_admin_attendance(request):
    subject_id = request.POST.get('subject')
    session_id = request.POST.get('session')
    attendance_date_id = request.POST.get('attendance_date_id')
    try:
        subject = get_object_or_404(Subject, id=subject_id)
        session = get_object_or_404(Session, id=session_id)
        attendance = get_object_or_404(
            Attendance, id=attendance_date_id, session=session)
        attendance_reports = AttendanceReport.objects.filter(
            attendance=attendance)
        json_data = []
        for report in attendance_reports:
            data = {
                "status": str(report.status),
                "name": str(report.student)
            }
            json_data.append(data)
        return JsonResponse(json.dumps(json_data), safe=False)
    except Exception as e:
        return None


def admin_view_profile(request):
    admin = get_object_or_404(Admin, admin=request.user)
    form = AdminForm(request.POST or None, request.FILES or None,
                     instance=admin)
    context = {'form': form,
               'page_title': _('View/Edit Profile'),
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                passport = request.FILES.get('profile_pic') or None
                custom_user = admin.admin
                if password != None:
                    custom_user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    custom_user.profile_pic = passport_url
                custom_user.first_name = first_name
                custom_user.last_name = last_name
                custom_user.save()
                messages.success(request, _("Profile Updated!"))
                return redirect(reverse('admin_view_profile'))
            else:
                messages.error(request, _("Invalid Data Provided"))
        except Exception as e:
            messages.error(
                request, _("Error Occured While Updating Profile ") + str(e))
    return render(request, "hod_template/admin_view_profile.html", context)


def admin_notify_staff(request):
    staff = CustomUser.objects.filter(user_type=2)
    context = {
        'page_title': _("Send Notifications To Staff"),
        'allStaff': staff
    }
    return render(request, "hod_template/staff_notification.html", context)


def admin_notify_student(request):
    student = CustomUser.objects.filter(user_type=3)
    context = {
        'page_title': _("Send Notifications To Students"),
        'students': student
    }
    return render(request, "hod_template/student_notification.html", context)

def admin_notify_hr(request):
    hr = CustomUser.objects.filter(user_type=4)
    context = {
        'page_title': _("Send Notifications To Manager"),
        'hr': hr
    }
    return render(request, "hod_template/hr_notification.html", context)


@csrf_exempt
def send_student_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    student = get_object_or_404(Student, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': _("Student Management System"),
                'body': message,
                'click_action': reverse('student_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': student.admin.fcm_token
        }
        headers = {'Authorization':
                       'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationStudent(student=student, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
def send_hr_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    hr = get_object_or_404(HR, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': _("Student Management System"),
                'body': message,
                'click_action': reverse('hr_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': hr.admin.fcm_token
        }
        headers = {'Authorization':
                       'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationHR(hr=hr, feedback=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")

@csrf_exempt
def send_staff_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    staff = get_object_or_404(Staff, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': _("Student Management System"),
                'body': message,
                'click_action': reverse('staff_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': staff.admin.fcm_token
        }
        headers = {'Authorization':
                       'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationStaff(staff=staff, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")

def delete_staff(request, staff_id):
    staff = get_object_or_404(CustomUser, staff__id=staff_id)
    staff.delete()
    messages.success(request, _("Staff deleted successfully!"))
    return redirect(reverse('manage_staff'))


def delete_hr(request, hr_id):
    hr = get_object_or_404(CustomUser, hr__id=hr_id)
    hr.delete()
    messages.success(request, _("HR deleted successfully!"))
    return redirect(reverse('manage_hr'))


def delete_student(request, student_id):
    student = get_object_or_404(CustomUser, student__id=student_id)
    student.delete()
    messages.success(request, _("Student deleted successfully!"))
    return redirect(reverse('manage_student'))


def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    try:
        course.delete()
        messages.success(request, _("Course deleted successfully!"))
    except Exception:
        messages.error(
            request,
            _("Sorry, some students are assigned to this course already. Kindly change the affected student course and try again"))
    return redirect(reverse('manage_course'))


def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    messages.success(request, _("Subject deleted successfully!"))
    return redirect(reverse('manage_subject'))


def delete_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    news.delete()
    messages.success(request, _("New deleted successfully!"))
    return redirect(reverse('admin_news'))


def delete_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    try:
        session.delete()
        messages.success(request, _("Session deleted successfully!"))
    except Exception:
        messages.error(
            request, _("There are students assigned to this session. Please move them to another session."))
    return redirect(reverse('manage_session'))
