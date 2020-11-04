from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    employee_id = models.CharField(max_length=5, unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=False, blank=True)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    office_number = models.CharField(max_length=20, null=True, blank=True)
    personal_email = models.EmailField(null=True, blank=True)
    designation = models.CharField(max_length=50, null=True, blank=True)
    grade = models.CharField(max_length=2, null=True, blank=True)
    primary_manager = models.ForeignKey("self", on_delete=models.SET_DEFAULT, default=1)
    primary_function = models.ForeignKey("Function", on_delete=models.SET_DEFAULT, default=1)
    functional_manager = models.CharField(max_length=255, null=True, blank=True)
    work_shift_start = models.TimeField(null=True, default="09:00:00")
    employment_type = models.CharField(max_length=10, null=True, blank=True)
    employment_status = models.CharField(max_length=1, null=True, blank=True)
    date_of_joining = models.DateField(help_text="Format: YYYY-MM-DD")
    date_of_separation = models.DateField(null=True, blank=True, help_text="Format: YYYY-MM-DD")
    date_of_resignation = models.DateField(null=True, blank=True, help_text="Format: YYYY-MM-DD")
    change_effective_from = models.DateField(help_text="Format: YYYY-MM-DD")
    change_comment = models.CharField(max_length=255, null=False, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name="employee_created_by")
    created_date = models.DateTimeField(null=False, default='1900-01-01')
    modified_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name="employee_modified_by")
    modified_date = models.DateTimeField(null=False, default='1900-01-01')

    def _get_full_name(self):
        "Returns the person's full name."
        mn = ""
        ln = ""
        if len(self.middle_name) > 0:
            mn = ' %s' % (self.middle_name)
        if len(self.last_name) > 0:
            ln = ' %s' % (self.last_name)
        return "%s%s%s" % (self.first_name, mn, ln)

    employee_name = property(_get_full_name)

    def __int__(self):
        return self.id


class Function(models.Model):
    function_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)
    manager = models.ForeignKey(Employee, on_delete=models.SET_DEFAULT, default=1)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name="function_created_by")
    created_date = models.DateTimeField(null=False, default='1900-01-01')
    modified_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name="function_modified_by")
    modified_date = models.DateTimeField(null=False, default='1900-01-01')

    def __int__(self):
        return self.id


class Skill(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name="skill_created_by")
    created_date = models.DateTimeField(null=False, default='1900-01-01')
    modified_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name="skill_modified_by")
    modified_date = models.DateTimeField(null=False, default='1900-01-01')

    def __int__(self):
        return self.id


class EmployeeSkillMapping(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, default=1)
    skill = models.ForeignKey(Skill, on_delete=models.SET_DEFAULT, default=1)
    proficiency = models.IntegerField(default=5)
    interested = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name="employee_skill_mapping_created_by")
    created_date = models.DateTimeField(null=False, default='1900-01-01')
    modified_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name="employee_skill_mapping_modified_by")
    modified_date = models.DateTimeField(null=False, default='1900-01-01')

    def __int__(self):
        return self.id

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['employee', 'skill'], name='unique_employee_skill'),
        ]


class Project(models.Model):
    project_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name="project_created_by")
    created_date = models.DateTimeField(null=False, default='1900-01-01')
    modified_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name="project_modified_by")
    modified_date = models.DateTimeField(null=False, default='1900-01-01')

    def __int__(self):
        return self.id


class ProjectRole(models.Model):
    role = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name="project_role_created_by")
    created_date = models.DateTimeField(null=False, default='1900-01-01')
    modified_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name="project_role_modified_by")
    modified_date = models.DateTimeField(null=False, default='1900-01-01')

    def __int__(self):
        return self.id


class ProjectMapping(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey(Employee, on_delete=models.CASCADE)
    role = models.ForeignKey(ProjectRole, on_delete=models.SET_DEFAULT, default=1)
    skill = models.ForeignKey(Skill, on_delete=models.SET_DEFAULT, default=1)
    bandwidth = models.DecimalField(max_digits=3, decimal_places=2, default=1.00)
    comments = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name="project_mapping_created_by")
    created_date = models.DateTimeField(null=False, default='1900-01-01')
    modified_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name="project_mapping_modified_by")
    modified_date = models.DateTimeField(null=False, default='1900-01-01')

    def __int__(self):
        return self.id


class UserRoleMapping(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, unique=True)
    add_employee = models.BooleanField(default=False)
    add_function = models.BooleanField(default=False)
    add_project = models.BooleanField(default=False)
    manager_actions = models.BooleanField(default=False)
    team_salary_access = models.BooleanField(default=False)
    all_salary_access = models.BooleanField(default=False)
    all_access = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name="user_role_mapping_created_by")
    created_date = models.DateTimeField(null=False, default='1900-01-01')
    modified_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name="user_role_modified_by")
    modified_date = models.DateTimeField(null=False, default='1900-01-01')

    def __int__(self):
        return self.id


