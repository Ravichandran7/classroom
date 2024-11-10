from django.urls import path, include

from . import views
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView
from .views import LogoutView,CustomLogoutView


urlpatterns = [
    path('', views.user_login, name='login'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    ##path('', views.teacher_dashboard, name='teacher_dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/manage_assignments/', views.manage_assignments, name='manage_assignments'),
    path('teacher/manage_submissions/<int:assignment_id>/', views.manage_submissions, name='manage_submissions'),
    path('teacher/add_resources/', views.add_resources, name='add_resources'),
    path('teacher/notify_students/', views.notify_students, name='notify_students'),
    path('student/assignment_page/', views.assignment_page, name='assignment_page'),
    path('student/notification_page/', views.notification_page, name='notification_page'),
    path('student/resources/', views.view_resources, name='view_resources'),
    path('register/', views.register, name='register'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    ##path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('student/assignments/', views.list_assignments, name='list_assignments'),
    path('student/submit_assignment/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
    path('teacher/view_submissions/<int:assignment_id>/', views.view_submissions, name='view_submissions'),
    ##path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),  # Add this line for login/logout/password URLs
    path('teacher/track_student_progress/', views.track_student_progress, name='track_student_progress'),
]
