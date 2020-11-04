from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),

    path('project', views.project_list, name='project'),
    path('project/<int:id>', views.project, name='project_id'),
    path('project_role', views.project_role_list, name='project_role'),
    path('project_role_new', views.project_role_new, name='project_role_new'),
    path('project_role_edit/<int:id>', views.project_role_edit, name='project_role_edit'),
    path('project_role_delete/<int:id>', views.project_role_delete, name='project_role_delete'),
    path('project_mapping_new/<int:id>', views.project_mapping_new, name='project_mapping_new'),
    path('project_mapping_edit/<int:id>', views.project_mapping_edit, name='project_mapping_edit'),
    path('project_mapping_delete/<int:id>', views.project_mapping_delete, name='project_mapping_delete'),
    path('project_edit/<int:id>', views.project_edit, name='project_edit'),
    path('project_new', views.project_new, name='project_new'),

    path('function', views.function_list, name='function'),
    path('function/<int:id>', views.function, name='function_id'),
    path('function_new', views.function_new, name='function_new'),
    path('function_edit/<int:id>', views.function_edit, name='function_edit'),

    path('employee', views.employee_list, name='employee'),
    path('ex_employee', views.ex_employee_list, name='ex_employee'),
    path('resigned_employee', views.resigned_employee_list, name='resigned_employee'),
    path('employee_new', views.employee_new, name="employee_new"),
    path('employee_edit/<int:id>', views.employee_edit, name='employee_edit'),
    path('employee/<int:id>', views.employee, name='employee_id'),
    path('head_count_report', views.headcount_report, name="head_count_report"),
    path('user_access/<int:id>', views.set_user_access, name='user_access'),
    path('reset_password/<int:id>', views.reset_user_password, name='reset_password'),

    path('skill', views.skill_list, name='skill'),
    path('skill_new', views.skill_new, name='skill_new'),
    path('skill_edit/<int:id>', views.skill_edit, name='skill_edit'),
    path('skill_mapping_new', views.skill_mapping_new, name='skill_mapping_new'),
    path('my_skill', views.my_skill, name='my_skill'),
    path('skill_mapping_edit/<int:id>', views.skill_mapping_edit, name='skill_mapping_edit'),
    path('skill_mapping_delete/<int:id>', views.skill_mapping_delete, name='skill_mapping_delete'),
    path('skill_employee/<int:id>', views.skill_employee, name='skill_employee'),
]
