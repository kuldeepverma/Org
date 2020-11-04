from django.core.exceptions import PermissionDenied
from org.models import UserRoleMapping, Employee


def all_access(function):
    def wrap(request, *args, **kwargs):
        e = Employee.objects.get(user_id=request.user.pk)
        perm = UserRoleMapping.objects.get(employee_id=e.pk)
        if perm.all_access:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def add_employee_access(function):
    def wrap(request, *args, **kwargs):
        e = Employee.objects.get(user_id=request.user.pk)
        perm = UserRoleMapping.objects.get(employee_id=e.pk)
        if perm.all_access or perm.add_employee:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def add_function_access(function):
    def wrap(request, *args, **kwargs):
        e = Employee.objects.get(user_id=request.user.pk)
        perm = UserRoleMapping.objects.get(employee_id=e.pk)
        if perm.all_access or perm.add_function:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def add_project_access(function):
    def wrap(request, *args, **kwargs):
        e = Employee.objects.get(user_id=request.user.pk)
        perm = UserRoleMapping.objects.get(employee_id=e.pk)
        if perm.all_access or perm.add_project:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def manager_action_access(function):
    def wrap(request, *args, **kwargs):
        e = Employee.objects.get(user_id=request.user.pk)
        perm = UserRoleMapping.objects.get(employee_id=e.pk)
        if perm.all_access or perm.manager_actions:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def team_salary_access(function):
    def wrap(request, *args, **kwargs):
        e = Employee.objects.get(user_id=request.user.pk)
        perm = UserRoleMapping.objects.get(employee_id=e.pk)
        if perm.all_access or perm.team_salary_access:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def add_all_salary_access(function):
    def wrap(request, *args, **kwargs):
        e = Employee.objects.get(user_id=request.user.pk)
        perm = UserRoleMapping.objects.get(employee_id=e.pk)
        if perm.all_access or perm.all_salary_access:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
