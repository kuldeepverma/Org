from django.contrib import admin
from .models import Employee, Project, Function, ProjectRole, ProjectMapping
# Register your models here.


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'first_name', 'middle_name', 'last_name',)
    ordering = ('employee_id',)
    search_fields = ('employee_id', 'first_name', 'middle_name', 'last_name',)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'name', 'url',)
    ordering = ('name',)
    search_fields = ('project_id', 'name', 'url',)


class FunctionAdmin(admin.ModelAdmin):
    list_display = ('function_id', 'name', 'manager', 'description',)
    ordering = ('name',)
    search_fields = ('function_id', 'name', 'manager', 'description',)


class ProjectRoleAdmin(admin.ModelAdmin):
    list_display = ('role', 'description')
    ordering = ('role',)
    search_fields = ('role', 'description')


class ProjectMappingAdmin(admin.ModelAdmin):
    list_display = ('project.name', 'member.employee_name', 'project_role.role')
    ordering = ('project.name', )


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Function, FunctionAdmin)


