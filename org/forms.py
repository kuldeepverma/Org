from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Employee, Function, ProjectRole, ProjectMapping, Project, Skill
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import date
import datetime

# --------------- Employee Forms ------------------ #


class NewEmployeeForm(UserCreationForm):
    employee_id = forms.CharField(max_length=5, required=True)
    email = forms.EmailField()
    personal_email = forms.EmailField(required=False)
    first_name = forms.CharField(max_length=50, required=True)
    middle_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    mobile_number = forms.CharField(max_length=20, required=False)
    office_number = forms.CharField(max_length=20, required=False)
    designation = forms.CharField(max_length=50, required=False)
    grade = forms.CharField(max_length=2, required=False)
    primary_manager = forms.ChoiceField(label="Primary manager")
    primary_function = forms.ChoiceField(label="Function")
    functional_manager = forms.CharField(max_length=255, required=False)
    shift_start_time = forms.TimeField(initial="12:00:00", required=False)
    employment_type = forms.ChoiceField()
    date_of_joining = forms.DateField(required=True, help_text="Format: YYYY-MM-DD")

    def __init__(self, *args, **kwargs):
        super(NewEmployeeForm, self).__init__(*args, **kwargs)
        del self.fields['password1']
        del self.fields['password2']
        manager_choices = []
        for iemployee in Employee.objects.all().order_by("first_name","middle_name","last_name"):
            manager_choices.append((iemployee.pk, iemployee.employee_name+" ("+str(iemployee.employee_id)+")"))
        function_choices = []
        for ifunction in Function.objects.all().order_by("name"):
            function_choices.append((ifunction.id, ifunction.name))
        employment_types = (("FTE", "Permanent Employee"), ("CONTRACT", "Contractor"),)
        self.fields['employee_id'].initial=int(Employee.objects.all().exclude(Q(employee_id__contains='C')).order_by("-employee_id")[0].employee_id) + 1
        self.fields['primary_function'].choices = function_choices
        self.fields['primary_manager'].choices = manager_choices
        self.fields['employment_type'].choices = employment_types

    class Meta:
        model = User
        fields = ()


class EditEmployeeForm(forms.Form):
    employee_id = forms.CharField(max_length=5, required=True)
    first_name = forms.CharField(max_length=50)
    middle_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    mobile_number = forms.CharField(max_length=20, required=False)
    office_number = forms.CharField(max_length=20, required=False)
    email = forms.EmailField()
    personal_email = forms.EmailField(required=False)
    designation = forms.CharField(max_length=50, required=False)
    grade = forms.CharField(max_length=2, required=False)
    primary_manager_id = forms.ChoiceField(label="Primary manager")
    primary_function_id = forms.ChoiceField(label="Function")
    functional_manager = forms.CharField(max_length=255, required=False)
    shift_start_time = forms.TimeField(required=False)
    employment_type = forms.ChoiceField()
    employment_status = forms.ChoiceField()
    date_of_joining = forms.DateField()
    date_of_resignation = forms.DateField(required=False)
    date_of_separation = forms.DateField(required=False)
    change_effective_from = forms.DateField(required=True, help_text="Format: YYYY-MM-DD")
    reason_for_change = forms.CharField(max_length=255, min_length=5, label="Reason for change in data")

    def __init__(self, *args, **kwargs):
        super(EditEmployeeForm, self).__init__(*args, **kwargs)
        manager_choices = []
        for iemployee in Employee.objects.all().order_by("first_name","middle_name","last_name"):
            manager_choices.append((iemployee.pk, iemployee.employee_name+" ("+str(iemployee.employee_id)+")"))
        function_choices = []
        for ifunction in Function.objects.all().order_by("name"):
            function_choices.append((ifunction.id, ifunction.name))
        employment_types = (("FTE", "Permanent Employee"), ("CONTRACT", "Contractor"),)
        employment_statuses = (("A", "Active"), ("R", "Resigned"), ("S", "Separated"),)
        self.fields['primary_function_id'].choices = function_choices
        self.fields['primary_manager_id'].choices = manager_choices
        self.fields['employment_type'].choices = employment_types
        self.fields['employment_status'].choices = employment_statuses
        self.fields['change_effective_from'].initial=datetime.date.today


# --------------- Project Forms ------------------ #


class NewProjectForm(forms.Form):
    project_id = forms.IntegerField()
    name = forms.CharField(max_length=50)
    url = forms.CharField(max_length=255, required=False)
    description = forms.CharField(max_length=255, required=False)
    manager_id = forms.ChoiceField(label='Manager')
    owner_id = forms.ChoiceField(required=False, label="Owner")
    ba_id = forms.ChoiceField(required=False, label="Business Analyst")

    def __init__(self, *args, **kwargs):
        super(NewProjectForm, self).__init__(*args, **kwargs)
        max_id = Project.objects.all().order_by("-project_id")[0].project_id + 1
        manager_choices = []
        owner_choices = []
        ba_choices = []
        owner_choices.append((1,''))
        ba_choices.append((1,''))
        employee_list = Employee.objects.all().order_by("first_name", "middle_name", "last_name")
        for iemployee in employee_list:
            if iemployee.id > 1:
                manager_choices.append((iemployee.id, iemployee.employee_name + " (" + str(iemployee.employee_id) + ")"))
                owner_choices.append((iemployee.id, iemployee.employee_name + " (" + str(iemployee.employee_id) + ")"))
                ba_choices.append((iemployee.id, iemployee.employee_name + " (" + str(iemployee.employee_id) + ")"))
        self.fields['project_id'].initial = max_id
        self.fields['manager_id'].choices = manager_choices
        self.fields['owner_id'].choices = owner_choices
        self.fields['ba_id'].choices = ba_choices

    class Meta:
        model = Project
        fields = '__all__'


class EditProjectForm(forms.Form):
    project_id = forms.IntegerField()
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=255, required=False)
    url = forms.CharField(max_length=255, required=False)


class NewProjectRoleForm(forms.Form):
    role = forms.CharField(max_length=50)
    role_description = forms.CharField(max_length=200)

    class Meta:
        model = ProjectRole
        fields = ('role', 'role_description')


class NewProjectMappingForm(forms.Form):
    member = forms.ChoiceField()
    project_role = forms.ChoiceField()
    skill = forms.ChoiceField()
    bandwidth = forms.DecimalField(initial=1.00, max_value=1.00, min_value=0.01)
    def __init__(self, *args, **kwargs):
        super(NewProjectMappingForm, self).__init__(*args, **kwargs)
        member_choices = []
        project_role_choices = []
        skill_choices = []
        employee_list = Employee.objects.all().exclude(id=1).order_by("first_name", "middle_name", "last_name")
        project_role_list = ProjectRole.objects.all().exclude(id=1).order_by("role")
        skill_list = Skill.objects.all().exclude(id=1).order_by("name")
        for iemployee in employee_list:
            member_choices.append((iemployee.id, iemployee.employee_name+" ("+str(iemployee.employee_id)+")"))
        for iprojectrole in project_role_list:
            project_role_choices.append((iprojectrole.id, iprojectrole.role))
        for iskill in skill_list:
            skill_choices.append((iskill.id, iskill.name))
        self.fields['member'].choices = member_choices
        self.fields['project_role'].choices = project_role_choices
        self.fields['skill'].choices = skill_choices

    class Meta:
        model=ProjectMapping
        fields = ('project', 'member', 'role')


# --------------- Function Forms ------------------ #


class NewFunctionForm(forms.Form):
    function_id = forms.IntegerField()
    name = forms.CharField(max_length=50)
    manager_id = forms.ChoiceField()
    description = forms.CharField(max_length=255, required=False)

    def __init__(self, *args, **kwargs):
        super(NewFunctionForm, self).__init__(*args, **kwargs)
        max_id = Function.objects.all().order_by("-function_id")[0].function_id + 1
        employee_list = Employee.objects.all().exclude(id=1).order_by("first_name", "middle_name", "last_name")
        manager_choices = []
        for iemployee in employee_list:
            manager_choices.append((iemployee.id, iemployee.employee_name + " (" + str(iemployee.employee_id) + ")"))
        self.fields['function_id'].initial = max_id
        self.fields['manager_id'].choices = manager_choices
    class Meta:
        model = Project
        fields = '__all__'


# ------------- Authorization Forms ---------------- #

class SetAuthorizationForm(forms.Form):
    add_employee = forms.BooleanField(initial=False, required=False)
    add_function = forms.BooleanField(initial=False, required=False)
    add_project = forms.BooleanField(initial=False, required=False)
    manager_actions = forms.BooleanField(initial=False, required=False)
    team_salary_access = forms.BooleanField(initial=False, required=False)
    all_salary_access = forms.BooleanField(initial=False, required=False)
    all_access = forms.BooleanField(initial=False, required=False)


# -------------- Skill Forms ----------------- #


class NewSkillForm(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Skill
        fields = '__all__'


class NewSkillMappingForm(forms.Form):
    skill = forms.ChoiceField()
    proficiency = forms.IntegerField(initial=5, max_value=10, min_value=1)
    interested = forms.BooleanField(initial=False, required=False)
    def __init__(self, *args, **kwargs):
        super(NewSkillMappingForm, self).__init__(*args, **kwargs)
        skill_choices = []
        skill_list = Skill.objects.all().exclude(id=1).order_by("name")
        for iskill in skill_list:
            skill_choices.append((iskill.id, iskill.name))
        self.fields['skill'].choices = skill_choices


# ---------------------- Report Forms --------------------- #


class HeadCountReport(forms.Form):
    start_date = forms.DateField(help_text="Format: YYYY-MM-DD")
    end_date = forms.DateField(help_text="Format: YYYY-MM-DD")



