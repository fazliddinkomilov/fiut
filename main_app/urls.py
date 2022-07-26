"""student_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from main_app.EditResultView import EditResultView

from . import hod_views, staff_views, student_views, views, hr_views
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.login_page, name='login_page'),
    path("get_attendance", views.get_attendance, name='get_attendance'),
    path("firebase-messaging-sw.js", views.showFirebaseJS, name='showFirebaseJS'),
    path("doLogin/", views.doLogin, name='user_login'),
    path("logout_user/", views.logout_user, name='user_logout'),
    path("admin/news/", hod_views.admin_news,
         name='admin_news'),
    path("admin/home/", hod_views.admin_home, name='admin_home'),
    path("staff/add", hod_views.add_staff, name='add_staff'),
    path("hr/add", hod_views.add_hr, name='add_hr'),
    path("news/add", hod_views.add_news, name='add_news'),
    path("course/add", hod_views.add_course, name='add_course'),
    path("send_student_notification/", hod_views.send_student_notification,
         name='send_student_notification'),
    path("send_hr_notification/", hod_views.send_hr_notification,
         name='send_hr_notification'),
    path("send_staff_notification/", hod_views.send_staff_notification,
         name='send_staff_notification'),
    path("add_session/", hod_views.add_session, name='add_session'),
    path("admin_notify_student", hod_views.admin_notify_student,
         name='admin_notify_student'),
    path("admin_notify_staff", hod_views.admin_notify_staff,
         name='admin_notify_staff'),
    path("admin_notify_hr", hod_views.admin_notify_hr,
         name='admin_notify_hr'),
    path("admin_view_profile", hod_views.admin_view_profile,
         name='admin_view_profile'),
    path("check_email_availability", hod_views.check_email_availability,
         name="check_email_availability"),
    path("session/manage/", hod_views.manage_session, name='manage_session'),
    path("session/edit/<int:session_id>",
         hod_views.edit_session, name='edit_session'),
    path("student/view/feedback/", hod_views.student_feedback_message,
         name="student_feedback_message",),
    path("staff/view/feedback/", hod_views.staff_feedback_message,
         name="staff_feedback_message",),
    path("student/view/leave/", hod_views.view_student_leave,
         name="view_student_leave",),
    path("staff/view/leave/", hod_views.view_staff_leave, name="view_staff_leave",),
    path("attendance/view/", hod_views.admin_view_attendance,
         name="admin_view_attendance",),
    path("attendance/fetch/", hod_views.get_admin_attendance,
         name='get_admin_attendance'),
    path("student/add/", hod_views.add_student, name='add_student'),
    path("subject/add/", hod_views.add_subject, name='add_subject'),
    path("staff/manage/", hod_views.manage_staff, name='manage_staff'),
    path("hr/manage/", hod_views.manage_hr, name='manage_hr'),
    path("student/manage/", hod_views.manage_student, name='manage_student'),
    path("course/manage/", hod_views.manage_course, name='manage_course'),
    path("subject/manage/", hod_views.manage_subject, name='manage_subject'),
    path("staff/edit/<int:staff_id>", hod_views.edit_staff, name='edit_staff'),
    path("hr/edit/<int:hr_id>", hod_views.edit_hr, name='edit_hr'),
    path("staff/delete/<int:staff_id>",
         hod_views.delete_staff, name='delete_staff'),

    path("hr/delete/<int:hr_id>",
         hod_views.delete_hr, name='delete_hr'),

    path("course/delete/<int:course_id>",
         hod_views.delete_course, name='delete_course'),

    path("subject/delete/<int:subject_id>",
         hod_views.delete_subject, name='delete_subject'),

    path("news/delete/<int:news_id>",
         hod_views.delete_news, name='delete_news'),

    path("session/delete/<int:session_id>",
         hod_views.delete_session, name='delete_session'),

    path("student/delete/<int:student_id>",
         hod_views.delete_student, name='delete_student'),
    path("student/edit/<int:student_id>",
         hod_views.edit_student, name='edit_student'),
    path("course/edit/<int:course_id>",
         hod_views.edit_course, name='edit_course'),
    path("subject/edit/<int:subject_id>",
         hod_views.edit_subject, name='edit_subject'),




    # Staff
    path("staff/home/",staff_views.staff_news,
         name='staff_home'),
    path("staff/news/", staff_views.staff_news,
         name='staff_news'),
    path("staff/apply/leave/", staff_views.staff_apply_leave,
         name='staff_apply_leave'),
    path("staff/feedback/", staff_views.staff_feedback, name='staff_feedback'),
    path("staff/view/profile/", staff_views.staff_view_profile,
         name='staff_view_profile'),
    path("staff/attendance/take/", staff_views.staff_take_attendance,
         name='staff_take_attendance'),
    path("staff/attendance/update/", staff_views.staff_update_attendance,
         name='staff_update_attendance'),
    path("staff/get_students/", staff_views.get_students, name='get_students'),
    path("staff/attendance/fetch/", staff_views.get_student_attendance,
         name='get_student_attendance'),
    path("staff/attendance/save/",
         staff_views.save_attendance, name='save_attendance'),
    path("staff/attendance/update/",
         staff_views.update_attendance, name='update_attendance'),
    path("staff/fcmtoken/", staff_views.staff_fcmtoken, name='staff_fcmtoken'),
    path("staff/view/notification/", staff_views.staff_view_notification,
         name="staff_view_notification"),
    path("staff/result/add/", staff_views.staff_add_result, name='staff_add_result'),
    path("staff/result/edit/", EditResultView.as_view(),
         name='edit_student_result'),
    path('staff/result/fetch/', staff_views.fetch_student_result,
         name='fetch_student_result'),

    # HR
    path("hr/home/", hr_views.hr_news,
         name='hr_home'),
    path("hr/news/", hr_views.hr_news,
         name='hr_news'),
    path("hr/apply/leave/", hr_views.hr_apply_leave,
         name='hr_apply_leave'),
    path("hr/feedback/", hr_views.hr_feedback, name='hr_feedback'),
    path("hr/view/profile/", hr_views.hr_view_profile,
         name='hr_view_profile'),
    path("hr/attendance/take/", hr_views.hr_take_attendance,
         name='hr_take_attendance'),
    path("hr/get_students/", hr_views.get_students, name='get_students'),
    path("hr/attendance/fetch/", hr_views.get_student_attendance,
         name='get_student_attendance'),
    path("hr/attendance/save/",
         hr_views.save_attendance, name='save_attendance'),
    path("hr/attendance/update/",
         hr_views.update_attendance, name='update_attendance'),
    path("hr/fcmtoken/", hr_views.hr_fcmtoken, name='hr_fcmtoken'),
    path("hr/view/notification/", hr_views.hr_view_notification,
         name="hr_view_notification"),
    path("hr/result/add/", hr_views.hr_add_result, name='hr_add_result'),
    path("hr/result/edit/", EditResultView.as_view(),
         name='edit_student_result'),
    path('hr/result/fetch/', hr_views.fetch_student_result,
         name='fetch_student_result'),


    # Student
    path("student/home/", student_views.student_news,
         name='student_home'),
    path("student/news/", student_views.student_news,
         name='student_news'),
    path("student/view/attendance/", student_views.student_view_attendance,
         name='student_view_attendance'),
    path("student/apply/leave/", student_views.student_apply_leave,
         name='student_apply_leave'),
    path("student/feedback/", student_views.student_feedback,
         name='student_feedback'),
    path("student/view/profile/", student_views.student_view_profile,
         name='student_view_profile'),
    path("student/fcmtoken/", student_views.student_fcmtoken,
         name='student_fcmtoken'),
    path("student/view/notification/", student_views.student_view_notification,
         name="student_view_notification"),
    path('student/view/result/', student_views.student_view_result,
         name='student_view_result'),


    path('i18n/', include('django.conf.urls.i18n')),

]
