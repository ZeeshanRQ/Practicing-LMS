from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup, name='signup'),
    path('mark_attendence/', views.mark_attendence, name='mark_attendence'),
    path('apply_leave/', views.apply_leave, name='apply_leave'),
    path('approve_leave/<int:leave_id>/', views.approve_leave, name='approve_leave/'),
    path('my_leave_history/', views.my_leave_history, name='my_leave_history'),
    path('associate_employee/', views.associate_employee, name='associate_employee'),
    path('manager_attendance_history/', views.manager_attendance_history, name='manager_attendance_history'),
    path('manager_leave_history/', views.manager_leave_history, name='manager_leave_history'),
    path('associate_employee_admin/', views.associate_employee_admin, name='associate_employee_admin'),

]