from django.urls import path
from .views import *

urlpatterns = [
     path('', home_page, name='home_page'),
     path('principal/login', principal_login, name='principal_login'),
     path('principal/dashboard/', principal_dashboard, name='principal_dashboard'),
     path('logout/', logout_view, name='logout'),
     path('principal/manage-notifications/', manage_notifications, name='manage_notifications'),
     path('principal/edit-notification/<int:notification_id>/', edit_notification, name='edit_notification'),
     path('principal/delete-notification/<int:notification_id>/', delete_notification, name='delete_notification'),
     path('principal/list-students/', list_students, name='list_students'),
     path('principal/deleted-students/', deleted_students, name='deleted_students'),
     path('principal/soft-delete-student/<int:student_id>/', soft_delete_student, name='soft_delete_student'),
     path('principal/restore-student/<int:student_id>/', restore_student, name='restore_student'),
     path('principal/add-student/', add_student, name='add_student'),
     path('principal/edit-student/<int:student_id>/', edit_student, name='edit_student'),
     path('principal/delete-student/<int:student_id>/', delete_student, name='delete_student'),
     path('principal/add_teacher/', add_teacher, name='add_teacher'),
     path('principal/list-teachers/', list_teachers, name='list_teachers'),
     path('principal/edit-teacher/<int:teacher_id>/', edit_teacher, name='edit_teacher'),
     path('principal/delete-teacher/<int:teacher_id>/', delete_teacher, name='delete_teacher'),
     path('principal/view-teacher-details/<int:teacher_id>/', view_teacher_details, name='view_teacher_details'),
     path('principal/view-student-details/<int:student_id>/', view_student_details, name='view_student_details'),
     path('principal/view-attendance-records/', view_attendance_records, name='view_attendance_records'),
     path('principal/view-performance-reports/', view_performance_reports, name='view_performance_reports'),



     path('teacher/login/', teacher_login, name='teacher_login'),
     path('teacher/dashboard/', teachers_dashboard, name='teachers_dashboard'),
     path('teacher/add-attendance/', add_attendance, name='add_attendance'),
     path('teacher/list-attendance/', list_attendance, name='list_attendance'),

     path('principal/grades/', list_grades, name='list_grades'),
     path('principal/grades/add/', add_grade, name='add_grade'),
     path('principal/grades/delete/<int:grade_id>/', delete_grade, name='delete_grade'),

     path('students/<int:student_id>/', student_profile, name='student_profile'),






     path('check-aadhaar/', check_aadhaar, name='check_aadhaar'),
     path('register/<int:student_id>/', register_student, name='register_student'),
     path('login/', student_login, name='login'),
     path('dashboard/', student_dashboard, name='student_dashboard'),




     path('file-complaint/', file_complaint, name='file_complaint'),
     path('complaints/', complaint_list, name='complaint_list'),
     path('resolve-complaint/<int:complaint_id>/', resolve_complaint, name='resolve_complaint'),



     path('grades/<int:grade_id>/subjects/add/', add_grade_subjects, name='add_grade_subjects'),
     path('assign-subjects/', assign_subjects_view, name='assign_subjects'),
     path('teacher-subjects/', teacher_subjects, name='teacher_subjects'),
     path('not-authorized/', not_authorized, name='not_authorized'),
     path('grades/<int:grade_id>/', grade_detail, name='grade_detail'),



     path('profile/', student_profile, name='student_profile'),
    # other paths...



]