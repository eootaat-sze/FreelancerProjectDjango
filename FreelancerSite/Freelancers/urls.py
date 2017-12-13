from django.urls import path

from . import views

app_name = 'freelancers'
urlpatterns = [
    path('', views.index, name='index'),
    path('projects', views.projects, name='projects'),
    path('freelancers', views.freelancers, name='freelancers'),
    path('login', views.login, name='login'),
    path('register_freelancer', views.register_freelancer, name='fre_reg'),
    path('register_employer', views.register_employer, name='emp_reg'),
    path('emp/<str:emp_email>', views.emp_projects, name='emp_projects'),
    path('fl/<str:fl_email>', views.fl_projects, name='fl_projects'),
    path('logout', views.logout, name='logout')
]