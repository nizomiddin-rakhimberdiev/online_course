from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('course/<int:course_id>/purchase/', views.purchase_course, name='purchase_course'),
    path('my-courses/', views.my_courses, name='my_courses'),

    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
