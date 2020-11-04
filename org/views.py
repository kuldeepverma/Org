from django.shortcuts import render, redirect
from .models import Function, Employee, Project, ProjectRole, ProjectMapping, UserRoleMapping, Skill, \
    EmployeeSkillMapping
from .forms import NewEmployeeForm, NewProjectForm, NewProjectMappingForm, NewProjectRoleForm, NewFunctionForm, \
    EditProjectForm, EditEmployeeForm, SetAuthorizationForm, NewSkillForm, NewSkillMappingForm, HeadCountReport
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .decorators import add_employee_access, add_function_access, add_project_access, all_access
from django.db.models import Q
from datetime import datetime, date, timedelta
#import datetime


# Create your views here.


def index(request):
    return render(request, 'org_index.html')


def check_access_level(request, perm):
    emp = Employee.objects.get(user_id=request.user.pk)
    p = UserRoleMapping.objects.get(employee_id=emp.id)
    if perm == 'add_employee':
        if p.add_employee == True or p.all_access == True:
            return 1
    elif perm == 'add_function':
        if p.add_function == True or p.all_access == True:
            return 1
    elif perm == 'add_project':
        if p.add_project == True or p.all_access == True:
            return 1
    elif perm == 'manager_actions':
        if p.manager_actions == True or p.all_access == True:
            return 1
    elif perm == 'team_salary_access':
        if p.team_salary_access == True or p.all_access == True:
            return 1
    elif perm == 'all_salary_access':
        if p.all_salary_access == True or p.all_access == True:
            return 1
    elif perm == 'all_access':
        if p.all_access == True:
            return True
    return False


# ------------ Employee Views --------------- #


@login_required
def employee_list(request):
    order_by = request.GET.get('sort', 'employee_id')
    asc_desc = request.GET.get('order', 'asc')
    if order_by == "employee_name":
        if asc_desc == "asc":
            employee_list = Employee.objects.all().exclude(id=1).order_by("first_name", "middle_name", "last_name")
        else:
            employee_list = Employee.objects.all().exclude(id=1).order_by("-first_name", "-middle_name", "-last_name")
    elif order_by == "manager_name":
        if asc_desc == "asc":
            employee_list = Employee.objects.all().exclude(id=1).order_by("primary_manager__first_name",
                                                                          "primary_manager__middle_name",
                                                                          "primary_manager__last_name")
        else:
            employee_list = Employee.objects.all().exclude(id=1).order_by("-primary_manager__first_name",
                                                                          "-primary_manager__middle_name",
                                                                          "-primary_manager__last_name")
    elif order_by == "function_name":
        if asc_desc == "asc":
            employee_list = Employee.objects.all().exclude(id=1).order_by("primary_function__name")
        else:
            employee_list = Employee.objects.all().exclude(id=1).order_by("-primary_function__name")
    elif order_by == "function_manager":
        if asc_desc == "asc":
            employee_list = Employee.objects.all().exclude(id=1).order_by("primary_function__manager__first_name",
                                                                          "primary_function__manager__middle_name",
                                                                          "primary_function__manager__last_name")
        else:
            employee_list = Employee.objects.all().exclude(id=1).order_by("-primary_function__manager__first_name",
                                                                          "-primary_function__manager__middle_name",
                                                                          "-primary_function__manager__last_name")
    else:
        if asc_desc == 'desc':
            employee_list = Employee.objects.all().exclude(id=1).order_by("-" + order_by)
        else:
            employee_list = Employee.objects.all().exclude(id=1).order_by(order_by)
    employee_list = employee_list.exclude(employment_status='S')
    query = request.GET.get('q')
    if query:
        object_list = employee_list.filter(
            Q(employee_id__icontains=query)
            | Q(first_name__icontains=query)
            | Q(middle_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(designation__icontains=query)
            | Q(primary_manager__first_name__icontains=query)
            | Q(primary_manager__middle_name__icontains=query)
            | Q(primary_manager__last_name__icontains=query)
            | Q(functional_manager__icontains=query)
            | Q(primary_function__name__icontains=query)
        )
        employee_list = object_list
    context = {'employee_list': employee_list, 'add_employee_access': check_access_level(request, 'add_employee')}
    return render(request, "emp/employee_view.html", context)


@login_required
@add_employee_access
def resigned_employee_list(request):
    order_by = request.GET.get('sort', 'date_of_separation')
    asc_desc = request.GET.get('order', 'desc')
    if order_by == "employee_name":
        if asc_desc == "asc":
            employee_list = Employee.objects.filter(employment_status='R').exclude(id=1).order_by("first_name",
                                                                                                  "middle_name",
                                                                                                  "last_name")
        else:
            employee_list = Employee.objects.filter(employment_status='R').exclude(id=1).order_by("-first_name",
                                                                                                  "-middle_name",
                                                                                                  "-last_name")
    elif order_by == "manager_name":
        if asc_desc == "asc":
            employee_list = Employee.objects.filter(employment_status='R').exclude(id=1).order_by(
                "primary_manager__first_name",
                "primary_manager__middle_name",
                "primary_manager__last_name")
        else:
            employee_list = Employee.objects.filter(employment_status='R').exclude(id=1).order_by(
                "-primary_manager__first_name",
                "-primary_manager__middle_name",
                "-primary_manager__last_name")
    elif order_by == "function_name":
        if asc_desc == "asc":
            employee_list = Employee.objects.filter(employment_status='R').exclude(id=1).order_by(
                "primary_function__name")
        else:
            employee_list = Employee.objects.filter(employment_status='R').exclude(id=1).order_by(
                "-primary_function__name")
    elif order_by == "function_manager":
        if asc_desc == "asc":
            employee_list = Employee.objects.filter(employment_status='R').exclude(id=1).order_by(
                "primary_function__manager__first_name",
                "primary_function__manager__middle_name",
                "primary_function__manager__last_name")
        else:
            employee_list = Employee.objects.filter(employment_status='R').exclude(id=1).order_by(
                "-primary_function__manager__first_name",
                "-primary_function__manager__middle_name",
                "-primary_function__manager__last_name")
    else:
        if asc_desc == 'desc':
            employee_list = Employee.objects.filter(employment_status='R').exclude(id=1).order_by("-" + order_by)
        else:
            employee_list = Employee.objects.filter(employment_status='R').exclude(id=1).order_by(order_by)
    query = request.GET.get('q')
    if query:
        object_list = employee_list.filter(
            Q(employee_id__icontains=query)
            | Q(first_name__icontains=query)
            | Q(middle_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(designation__icontains=query)
            | Q(primary_manager__first_name__icontains=query)
            | Q(primary_manager__middle_name__icontains=query)
            | Q(primary_manager__last_name__icontains=query)
            | Q(functional_manager__icontains=query)
            | Q(primary_function__name__icontains=query)
        )
        employee_list = object_list
    context = {'employee_list': employee_list, 'add_employee_access': check_access_level(request, 'add_employee')}
    return render(request, "emp/resigned_employee_view.html", context)


@login_required
@add_employee_access
def ex_employee_list(request):
    order_by = request.GET.get('sort', 'date_of_separation')
    asc_desc = request.GET.get('order', 'desc')
    if order_by == "employee_name":
        if asc_desc == "asc":
            employee_list = Employee.objects.filter(employment_status='S').exclude(id=1).order_by("first_name",
                                                                                                  "middle_name",
                                                                                                  "last_name")
        else:
            employee_list = Employee.objects.filter(employment_status='S').exclude(id=1).order_by("-first_name",
                                                                                                  "-middle_name",
                                                                                                  "-last_name")
    elif order_by == "manager_name":
        if asc_desc == "asc":
            employee_list = Employee.objects.filter(employment_status='S').exclude(id=1).order_by(
                "primary_manager__first_name",
                "primary_manager__middle_name",
                "primary_manager__last_name")
        else:
            employee_list = Employee.objects.filter(employment_status='S').exclude(id=1).order_by(
                "-primary_manager__first_name",
                "-primary_manager__middle_name",
                "-primary_manager__last_name")
    elif order_by == "function_name":
        if asc_desc == "asc":
            employee_list = Employee.objects.filter(employment_status='S').exclude(id=1).order_by(
                "primary_function__name")
        else:
            employee_list = Employee.objects.filter(employment_status='S').exclude(id=1).order_by(
                "-primary_function__name")
    elif order_by == "function_manager":
        if asc_desc == "asc":
            employee_list = Employee.objects.filter(employment_status='S').exclude(id=1).order_by(
                "primary_function__manager__first_name",
                "primary_function__manager__middle_name",
                "primary_function__manager__last_name")
        else:
            employee_list = Employee.objects.filter(employment_status='S').exclude(id=1).order_by(
                "-primary_function__manager__first_name",
                "-primary_function__manager__middle_name",
                "-primary_function__manager__last_name")
    else:
        if asc_desc == 'desc':
            employee_list = Employee.objects.filter(employment_status='S').exclude(id=1).order_by("-" + order_by)
        else:
            employee_list = Employee.objects.filter(employment_status='S').exclude(id=1).order_by(order_by)
    query = request.GET.get('q')
    if query:
        object_list = employee_list.filter(
            Q(employee_id__icontains=query)
            | Q(first_name__icontains=query)
            | Q(middle_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(designation__icontains=query)
            | Q(primary_manager__first_name__icontains=query)
            | Q(primary_manager__middle_name__icontains=query)
            | Q(primary_manager__last_name__icontains=query)
            | Q(functional_manager__icontains=query)
            | Q(primary_function__name__icontains=query)
        )
        employee_list = object_list
    context = {'employee_list': employee_list, 'add_employee_access': check_access_level(request, 'add_employee')}
    return render(request, "emp/ex_employee_view.html", context)


@login_required
def employee(request, id):
    e = Employee.objects.get(id=id)
    shift_end = e.work_shift_start.replace(hour=(e.work_shift_start.hour + 9) % 24)
    context = {'employee': e,
               'projects': ProjectMapping.objects.filter(member_id=id),
               'reportees': Employee.objects.filter(primary_manager_id=id).order_by("first_name", "middle_name",
                                                                                    "last_name"),
               'skills': EmployeeSkillMapping.objects.filter(employee_id=id).order_by("-interested","-proficiency"),
               'add_employee_access': check_access_level(request, 'add_employee'),
               'all_access': check_access_level(request, 'all_access'),
               'shift_end': shift_end}
    return render(request, 'emp/employee.html', context)


@login_required
@add_employee_access
def employee_new(request):
    if request.method == 'POST':
        form = NewEmployeeForm(request.POST)
        if form.is_valid():
            employee_id = form.cleaned_data['employee_id']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            middle_name = form.cleaned_data['middle_name']
            last_name = form.cleaned_data['last_name']
            mobile_number = form.cleaned_data['mobile_number']
            office_number = form.cleaned_data['office_number']
            designation = form.cleaned_data['designation']
            grade = form.cleaned_data['grade']
            primary_manager = form.cleaned_data['primary_manager']
            primary_function = form.cleaned_data['primary_function']
            employment_type = form.cleaned_data['employment_type']
            date_of_joining = form.cleaned_data['date_of_joining']
            functional_manager = form.cleaned_data['functional_manager']
            work_shift_start = form.cleaned_data['shift_start_time']
            change_effective_from = date_of_joining
            change_comment = "Initial Record"
            personal_email = form.cleaned_data['personal_email']
            user = User.objects.create_user(first_name=first_name, username=email, email=email, password="Welcome!")

            e = Employee(employee_id=employee_id,
                         first_name=first_name,
                         middle_name=middle_name,
                         last_name=last_name,
                         mobile_number=mobile_number,
                         office_number=office_number,
                         designation=designation,
                         grade=grade,
                         primary_manager_id=primary_manager,
                         primary_function_id=primary_function,
                         employment_type=employment_type,
                         date_of_joining=date_of_joining,
                         employment_status="A",
                         user_id=user.pk,
                         email=user.email,
                         functional_manager=functional_manager,
                         work_shift_start=work_shift_start,
                         created_by=request.user,
                         created_date=datetime.now(),
                         modified_by=request.user,
                         modified_date=datetime.now(),
                         change_effective_from=change_effective_from,
                         change_comment=change_comment,
                         personal_email=personal_email)
            e.save()
            ea = UserRoleMapping(employee_id=e.pk,
                                 created_by=request.user,
                                 created_date=datetime.now(),
                                 modified_by=request.user,
                                 modified_date=datetime.now())
            ea.save()
            return redirect('/org/employee')
    else:
        form = NewEmployeeForm()
    return render(request, 'emp/employee_new.html', {'form': form})


@login_required
@add_employee_access
def employee_edit(request, id):
    if request.method == 'POST':
        form = EditEmployeeForm(request.POST)
        if form.is_valid():
            new_employee_id = form.cleaned_data['employee_id']
            new_first_name = form.cleaned_data['first_name']
            new_middle_name = form.cleaned_data['middle_name']
            new_last_name = form.cleaned_data['last_name']
            new_mobile_number = form.cleaned_data['mobile_number']
            new_office_number = form.cleaned_data['office_number']
            new_email = form.cleaned_data['email']
            new_designation = form.cleaned_data['designation']
            new_grade = form.cleaned_data['grade']
            new_primary_manager_id = form.cleaned_data['primary_manager_id']
            new_primary_function_id = form.cleaned_data['primary_function_id']
            new_employment_type = form.cleaned_data['employment_type']
            new_employment_status = form.cleaned_data['employment_status']
            new_date_of_joining = form.cleaned_data['date_of_joining']
            new_date_of_resignation = form.cleaned_data['date_of_resignation']
            new_date_of_separation = form.cleaned_data['date_of_separation']
            new_functional_manager = form.cleaned_data['functional_manager']
            new_work_shift_start = form.cleaned_data['shift_start_time']
            change_effective_from = form.cleaned_data['change_effective_from']
            change_comment = form.cleaned_data['reason_for_change']
            personal_email = form.cleaned_data['personal_email']
            Employee.objects.filter(id=id).update(employee_id=new_employee_id,
                                                  first_name=new_first_name,
                                                  middle_name=new_middle_name,
                                                  last_name=new_last_name,
                                                  mobile_number=new_mobile_number,
                                                  office_number=new_office_number,
                                                  email=new_email,
                                                  designation=new_designation,
                                                  grade=new_grade,
                                                  primary_manager_id=new_primary_manager_id,
                                                  primary_function_id=new_primary_function_id,
                                                  employment_type=new_employment_type,
                                                  employment_status=new_employment_status,
                                                  date_of_joining=new_date_of_joining,
                                                  date_of_resignation=new_date_of_resignation,
                                                  date_of_separation=new_date_of_separation,
                                                  functional_manager=new_functional_manager,
                                                  work_shift_start=new_work_shift_start,
                                                  modified_by=request.user,
                                                  modified_date=datetime.now(),
                                                  change_effective_from=change_effective_from,
                                                  change_comment=change_comment,
                                                  personal_email=personal_email
                                                  )
            return redirect('/org/employee/' + str(id))
    else:
        e = Employee.objects.get(id=id)
        form = EditEmployeeForm({'employee_id': e.employee_id,
                                 'first_name': e.first_name,
                                 'middle_name': e.middle_name,
                                 'last_name': e.last_name,
                                 'mobile_number': e.mobile_number,
                                 'office_number': e.office_number,
                                 'email': e.email,
                                 'designation': e.designation,
                                 'grade': e.grade,
                                 'primary_manager_id': e.primary_manager.pk,
                                 'primary_function_id': e.primary_function.pk,
                                 'employment_type': e.employment_type,
                                 'employment_status': e.employment_status,
                                 'date_of_joining': e.date_of_joining,
                                 'date_of_resignation': e.date_of_resignation,
                                 'date_of_separation': e.date_of_separation,
                                 'functional_manager': e.functional_manager,
                                 'shift_start_time': e.work_shift_start
                                 })
    return render(request, 'emp/employee_new.html', {'form': form})



@login_required
@add_employee_access
def reset_user_password(request, id):
    e = Employee.objects.get(id=id)
    u = User.objects.get(id=e.user_id)
    u.set_password('Welcome!')
    u.save()
    return redirect('/org/employee/' + str(id))

# ------------ Function Views --------------- #


@login_required
def function_list(request):
    order_by = request.GET.get('sort', 'function_id')
    asc_desc = request.GET.get('order', 'asc')

    if order_by == "function_manager":
        if asc_desc == "asc":
            function_list = Function.objects.exclude(id=-1).order_by("manager__first_name",
                                                                     "manager__middle_name",
                                                                     "manager__last_name")
        else:
            function_list = Function.objects.all().order_by("-manager__first_name",
                                                            "-manager__middle_name",
                                                            "-manager__last_name")

    else:
        if asc_desc == 'desc':
            function_list = Function.objects.all().exclude(id=1).order_by("-" + order_by)
        else:
            function_list = Function.objects.all().exclude(id=1).order_by(order_by)
    query = request.GET.get('q')
    if query:
        object_list = function_list.filter(
            Q(function_id__icontains=query)
            | Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(manager__first_name__icontains=query)
            | Q(manager__middle_name__icontains=query)
            | Q(manager__last_name__icontains=query)
        )
        function_list = object_list
    context = {'function_list': function_list, 'add_function_access': check_access_level(request, 'add_function')}
    return render(request, "function/function_view.html", context)


def function(request, id):
    context = {'function': Function.objects.get(id=id),
               'employees': Employee.objects.filter(primary_function_id=id).order_by("first_name", "middle_name",
                                                                                     "last_name"),
               'add_function_access': check_access_level(request, 'add_function')}
    return render(request, 'function/function.html', context)


@login_required
@add_function_access
def function_new(request):
    if request.method == 'GET':
        form = NewFunctionForm()
    else:
        form = NewFunctionForm(request.POST)
        if form.is_valid():
            function_id = form.cleaned_data['function_id']
            name = form.cleaned_data['name']
            manager_id = form.cleaned_data['manager_id']
            description = form.cleaned_data['description']
            f = Function(function_id=function_id,
                         name=name,
                         manager_id=manager_id,
                         description=description,
                         created_by=request.user,
                         created_date=datetime.now(),
                         modified_by=request.user,
                         modified_date=datetime.now())
            f.save()
            return redirect('/org/function')
    return render(request, 'function/function_new.html', {'form': form})


@login_required
@add_function_access
def function_edit(request, id):
    if request.method == 'GET':
        f = Function.objects.get(id=id)
        form = NewFunctionForm(
            {'function_id': f.function_id, 'description': f.description, 'name': f.name, 'manager_id': f.manager_id})
    else:
        form = NewFunctionForm(request.POST)
        if form.is_valid():
            new_function_id = form.cleaned_data['function_id']
            new_name = form.cleaned_data['name']
            new_manager_id = form.cleaned_data['manager_id']
            new_description = form.cleaned_data['description']
            Function.objects.filter(id=id).update(function_id=new_function_id,
                                                  name=new_name,
                                                  manager_id=new_manager_id,
                                                  description=new_description,
                                                  modified_by=request.user,
                                                  modified_date=datetime.now())
            return redirect('/org/function')
    return render(request, 'function/function_new.html', {'form': form})


# ------------ Project Views --------------- #


@login_required
def project_list(request):
    order_by = request.GET.get('sort', 'project_id')
    asc_desc = request.GET.get('order', 'asc')
    if asc_desc == 'desc':
        project_list = Project.objects.all().exclude(id=1).order_by("-" + order_by)
    else:
        project_list = Project.objects.all().exclude(id=1).order_by(order_by)
    query = request.GET.get('q')
    if query:
        object_list = project_list.filter(
            Q(project_id__icontains=query)
            | Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(url__icontains=query)
        )
        project_list = object_list
    context = {'project_list': project_list, 'add_project_access': check_access_level(request, 'add_project')}
    return render(request, "project/project_view.html", context)


@login_required
def project(request, id):
    p = Project.objects.get(id=id)
    members = ProjectMapping.objects.filter(project_id=id)
    context = {'project': p, 'members': members, 'add_project_access': check_access_level(request, 'add_project')}
    return render(request, 'project/project.html', context)


@login_required
@add_project_access
def project_new(request):
    if request.method == 'GET':
        form = NewProjectForm()
    else:
        form = NewProjectForm(request.POST)
        if form.is_valid():
            project_id = form.cleaned_data['project_id']
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            url = form.cleaned_data['url']
            manager_id = form.cleaned_data['manager_id']
            owner_id = form.cleaned_data['owner_id']
            ba_id = form.cleaned_data['ba_id']
            p = Project(project_id=project_id,
                        name=name,
                        url=url,
                        description=description,
                        created_by=request.user,
                        created_date=datetime.now(),
                        modified_by=request.user,
                        modified_date=datetime.now())
            p.save()
            p.refresh_from_db()
            pm_role_id = ProjectRole.objects.get(role="Project Manager").id
            pm = ProjectMapping(project_id=p.id,
                                member_id=manager_id,
                                role_id=pm_role_id,
                                created_by=request.user,
                                created_date=datetime.now(),
                                modified_by=request.user,
                                modified_date=datetime.now())
            pm.save()
            if int(owner_id) > 1:
                po_role_id = ProjectRole.objects.get(role="Project Owner").id
                po = ProjectMapping(project_id=p.id,
                                    member_id=owner_id,
                                    role_id=po_role_id,
                                    created_by=request.user,
                                    created_date=datetime.now(),
                                    modified_by=request.user,
                                    modified_date=datetime.now())
                po.save()
            if int(ba_id) > 1:
                ba_role_id = ProjectRole.objects.get(role="Business Analyst")
                ba = ProjectMapping(project_id=p.id,
                                    member_id=ba_id,
                                    role_id=ba_role_id,
                                    created_by=request.user,
                                    created_date=datetime.now(),
                                    modified_by=request.user,
                                    modified_date=datetime.now())
                ba.save()
            return redirect('/org/project')
    return render(request, 'project/project_new.html', {'form': form})


@login_required
@add_project_access
def project_edit(request, id):
    if request.method == 'GET':
        p = Project.objects.get(id=id)
        form = EditProjectForm({'project_id': p.project_id, 'name': p.name, 'url': p.url, 'description': p.description})
    else:
        form = EditProjectForm(request.POST)
        if form.is_valid():
            new_project_id = form.cleaned_data['project_id']
            new_name = form.cleaned_data['name']
            new_url = form.cleaned_data['url']
            new_description = form.cleaned_data['description']
            Project.objects.filter(id=id).update(project_id=new_project_id,
                                                 name=new_name,
                                                 url=new_url,
                                                 description=new_description,
                                                 modified_by=request.user,
                                                 modified_date=datetime.now())
            return redirect('/org/project')
    return render(request, 'project/project_edit.html', {'form': form})


@login_required
def project_role_list(request):
    order_by = request.GET.get('sort', 'role')
    asc_desc = request.GET.get('order', 'asc')
    if asc_desc == 'desc':
        project_roles = ProjectRole.objects.all().order_by("-" + order_by)
    else:
        project_roles = ProjectRole.objects.all().order_by(order_by)
    query = request.GET.get('q')
    if query:
        object_list = project_roles.filter(
            Q(role__icontains=query)
            | Q(description__icontains=query)
        )
        project_roles = object_list
    context = {'project_roles': project_roles, 'add_project_access': check_access_level(request, 'add_project')}
    return render(request, "project/project_role_view.html", context)


@login_required
@add_project_access
def project_role_new(request):
    if request.method == 'GET':
        form = NewProjectRoleForm()
    else:
        form = NewProjectRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            role_description = form.cleaned_data['role_description']
            pr = ProjectRole(role=role,
                             description=role_description,
                             created_by=request.user,
                             created_date=datetime.now(),
                             modified_by=request.user,
                             modified_date=datetime.now())
            pr.save()
            return redirect('/org/project_role')
    return render(request, 'project/project_role_new.html', {'form': form})


@login_required
@add_project_access
def project_role_edit(request, id):
    pr = ProjectRole.objects.get(id=id)
    if request.method == 'GET':
        form = NewProjectRoleForm({'role': pr.role, 'role_description': pr.description})
    else:
        form = NewProjectRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            description = form.cleaned_data['role_description']
            ProjectRole.objects.filter(id=id).update(role=role,
                                                     description=description,
                                                     modified_by=request.user,
                                                     modified_date=datetime.now())
            return redirect('/org/project_role')
    return render(request, 'project/project_role_new.html', {'form': form})


@login_required
@add_project_access
def project_role_delete(request, id):
    ProjectRole.objects.filter(id=id).update(modified_by=request.user,
                                             modified_date=datetime.now())
    pr = ProjectRole.objects.get(id=id)
    pr.delete()
    return redirect('/org/project_role')


@login_required
@add_project_access
def project_mapping_new(request, id):
    project = Project.objects.get(id=id)
    if request.method == 'GET':
        form = NewProjectMappingForm()
    else:
        form = NewProjectMappingForm(request.POST)
        if form.is_valid():
            member_id = form.cleaned_data['member']
            project_id = project.pk
            project_role_id = form.cleaned_data['project_role']
            bandwidth = form.cleaned_data['bandwidth']
            skill_id = form.cleaned_data['skill']
            pm = ProjectMapping(member_id=member_id,
                                project_id=project_id,
                                role_id=project_role_id,
                                skill_id=skill_id,
                                bandwidth=bandwidth,
                                created_by=request.user,
                                created_date=datetime.now(),
                                modified_by=request.user,
                                modified_date=datetime.now())
            pm.save()
            return redirect('/org/project/' + str(project_id))
    return render(request, 'project/project_mapping_new.html', {'form': form})


@login_required
@add_project_access
def project_mapping_edit(request, id):
    pm = ProjectMapping.objects.get(id=id)
    if request.method == 'GET':
        form = NewProjectMappingForm({'member': pm.member_id, 'project_role': pm.role_id, 'bandwidth': pm.bandwidth, 'skill': pm.skill_id})
    else:
        form = NewProjectMappingForm(request.POST)
        if form.is_valid():
            member_id = form.cleaned_data['member']
            project_role_id = form.cleaned_data['project_role']
            skill_id = form.cleaned_data['skill']
            bandwidth = form.cleaned_data['bandwidth']
            ProjectMapping.objects.filter(id=id).update(member_id=member_id,
                                                        role_id=project_role_id,
                                                        skill_id=skill_id,
                                                        bandwidth=bandwidth,
                                                        modified_by=request.user,
                                                        modified_date=datetime.now())
            return redirect('/org/project/' + str(pm.project_id))
    return render(request, 'project/project_mapping_new.html', {'form': form})


@login_required
@add_project_access
def project_mapping_delete(request, id):
    ProjectMapping.objects.filter(id=id).update(modified_by=request.user,
                                                modified_date=datetime.now())
    pm = ProjectMapping.objects.get(id=id)
    project_id = pm.project_id
    pm.delete()
    return redirect('/org/project/' + str(project_id))


# ---------------------- user Access --------------------- #

@login_required
@all_access
def set_user_access(request, id):
    u = UserRoleMapping.objects.get(employee_id=id)
    employee_name = Employee.objects.get(id=id).employee_name
    employee_pk = Employee.objects.get(id=id).pk
    if request.method == 'GET':
        form = SetAuthorizationForm(
            {'user_id': u.employee_id, 'add_employee': u.add_employee, 'add_function': u.add_function,
             'add_project': u.add_project, 'manager_actions': u.manager_actions,
             'team_salary_Access': u.team_salary_access,
             'all_salary_access': u.all_salary_access, 'all_access': u.all_access})
    else:
        form = SetAuthorizationForm(request.POST)
        if form.is_valid():
            add_employee = form.cleaned_data['add_employee']
            add_function = form.cleaned_data['add_function']
            add_project = form.cleaned_data['add_project']
            manager_actions = form.cleaned_data['manager_actions']
            team_salary_access = form.cleaned_data['team_salary_access']
            all_salary_access = form.cleaned_data['all_salary_access']
            all_access = form.cleaned_data['all_access']
            UserRoleMapping.objects.filter(id=u.pk).update(employee_id=employee_pk,
                                                           add_employee=add_employee,
                                                           add_function=add_function,
                                                           add_project=add_project,
                                                           manager_actions=manager_actions,
                                                           team_salary_access=team_salary_access,
                                                           all_salary_access=all_salary_access,
                                                           all_access=all_access,
                                                           modified_by=request.user,
                                                           modified_date=datetime.now()
                                                           )
    return render(request, 'emp/employee_set_access.html', {'form': form, 'employee_name': employee_name})


# ------------ Skill Views --------------- #


@login_required
def skill_list(request):
    skill_list = Skill.objects.all().exclude(id=1)
    order_by = request.GET.get('sort', 'name')
    asc_desc = request.GET.get('order', 'asc')
    if asc_desc == 'desc':
        skill_list = skill_list.order_by("-" + order_by)
    else:
        skill_list = skill_list.order_by(order_by)
    query = request.GET.get('q')
    if query:
        object_list = skill_list.filter(
            Q(name__icontains=query)
        )
        skill_list = object_list

    context = {'skill_list': skill_list, 'add_project_access': check_access_level(request, 'add_project')}
    return render(request, "skill/skill_view.html", context)


@login_required
@add_project_access
def skill_new(request):
    if request.method == 'GET':
        form = NewSkillForm()
    else:
        form = NewSkillForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            pr = Skill(name=name,
                       description=description,
                       created_by=request.user,
                       created_date=datetime.now(),
                       modified_by=request.user,
                       modified_date=datetime.now())
            pr.save()
            return redirect('/org/skill')
    return render(request, 'skill/skill_new.html', {'form': form})


@login_required
@add_project_access
def skill_edit(request, id):
    pr = Skill.objects.get(id=id)
    if request.method == 'GET':
        form = NewSkillForm({'name': pr.name, 'description': pr.description})
    else:
        form = NewSkillForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            Skill.objects.filter(id=id).update(name=name,
                                               description=description,
                                               modified_by=request.user,
                                               modified_date=datetime.now())
            return redirect('/org/skill')
    return render(request, 'skill/skill_new.html', {'form': form})


@login_required
def my_skill(request):
    emp = Employee.objects.get(user_id=request.user.pk)
    order_by = request.GET.get('sort', 'name')
    asc_desc = request.GET.get('order', 'asc')
    if asc_desc == 'desc':
        if order_by == 'skill':
            skill_list = EmployeeSkillMapping.objects.filter(employee_id=emp.id).order_by("-skill__name")
        elif order_by == 'description':
            skill_list = EmployeeSkillMapping.objects.filter(employee_id=emp.id).order_by("-skill__description")
        else:
            skill_list = EmployeeSkillMapping.objects.filter(employee_id=emp.id).order_by("-proficiency")
    else:
        if order_by == 'skill':
            skill_list = EmployeeSkillMapping.objects.filter(employee_id=emp.id).order_by("skill__name")
        elif order_by == 'description':
            skill_list = EmployeeSkillMapping.objects.filter(employee_id=emp.id).order_by("skill__description")
        else:
            skill_list = EmployeeSkillMapping.objects.filter(employee_id=emp.id).order_by("proficiency")
    query = request.GET.get('q')
    if query:
        object_list = skill_list.filter(
            Q(skill__name__icontains=query)
            | Q(skill__description__icontains=query)
        )
        skill_list = object_list

    context = {'skill_list': skill_list}
    return render(request, "skill/my_skill.html", context)


@login_required
def skill_mapping_new(request):
    if request.method == 'GET':
        form = NewSkillMappingForm()
    else:
        form = NewSkillMappingForm(request.POST)
        if form.is_valid():
            emp = Employee.objects.get(user_id=request.user.pk)
            skill_id = form.cleaned_data['skill']
            member_id = emp.id
            proficiency = form.cleaned_data['proficiency']
            interested = form.cleaned_data['interested']
            sm = EmployeeSkillMapping(employee_id=member_id,
                                      skill_id=skill_id,
                                      proficiency=proficiency,
                                      created_by=request.user,
                                      created_date=datetime.now(),
                                      modified_by=request.user,
                                      modified_date=datetime.now(),
                                      interested=interested)
            sm.save()
            return redirect('/org/my_skill')
    return render(request, 'skill/skill_mapping_new.html', {'form': form})


@login_required
def skill_mapping_edit(request, id):
    sm = EmployeeSkillMapping.objects.get(id=id)
    if request.method == 'GET':
        form = NewSkillMappingForm({'skill': sm.skill_id, 'proficiency': sm.proficiency, 'interested': sm.interested})
    else:
        form = NewSkillMappingForm(request.POST)
        if form.is_valid():
            emp = Employee.objects.get(user_id=request.user.pk)
            skill_id = form.cleaned_data['skill']
            member_id = emp.id
            proficiency = form.cleaned_data['proficiency']
            interested = form.cleaned_data['interested']
            EmployeeSkillMapping.objects.filter(id=id).update(employee_id=member_id,
                                                              skill_id=skill_id,
                                                              proficiency=proficiency,
                                                              modified_by=request.user,
                                                              modified_date=datetime.now(),
                                                              interested=interested)
            return redirect('/org/my_skill')
    return render(request, 'skill/skill_mapping_new.html', {'form': form})


@login_required
def skill_mapping_delete(request, id):
    EmployeeSkillMapping.objects.filter(id=id).update(modified_by=request.user,
                                                      modified_date=datetime.now())
    sm = EmployeeSkillMapping.objects.get(id=id)
    sm.delete()
    return redirect('/org/my_skill')


@login_required
def skill_employee(request, id):
    skill = Skill.objects.get(id=id)
    members = EmployeeSkillMapping.objects.filter(skill_id=id).order_by("-interested", "-proficiency")
    context = {'members': members, 'skill': skill}
    return render(request, "skill/skill_employee.html", context)


# ---------------------- Reports --------------------- #


@login_required
@add_employee_access
def headcount_report(request):
    if request.method == 'GET':
        today = date.today()
        first = today.replace(day=1)
        last_month_last = first - timedelta(days=1)
        last_month_first = last_month_last.replace(day=1)
        active_employees = Employee.objects.all().exclude(id=1).filter(employment_status="A").exclude(
            date_of_resignation__lte=last_month_last).exclude(date_of_separation__lte=last_month_last)
        resigned_employees = Employee.objects.all().exclude(id=1).exclude(
            date_of_resignation__gt=last_month_last).exclude(date_of_resignation__lt=last_month_first).exclude(
            date_of_resignation__isnull=True)
        separated_employees = Employee.objects.all().exclude(id=1).exclude(
            date_of_separation__gt=last_month_last).exclude(date_of_separation__lt=last_month_first).exclude(
            date_of_separation__isnull=True)
        new_employees = Employee.objects.all().exclude(id=1).exclude(
            date_of_joining__gt=last_month_last).exclude(date_of_joining__lt=last_month_first).exclude(
            date_of_joining__isnull=True)
        form = HeadCountReport({'start_date': last_month_first, 'end_date': last_month_last})
    else:
        form = HeadCountReport(request.POST)
        if form.is_valid():
            last_month_first = form.cleaned_data['start_date']
            last_month_last = form.cleaned_data['end_date']
            active_employees = Employee.objects.all().exclude(id=1).exclude(
                date_of_resignation__lte=last_month_last).exclude(date_of_separation__lte=last_month_last)
            resigned_employees = Employee.objects.all().exclude(id=1).exclude(
                date_of_resignation__gt=last_month_last).exclude(date_of_resignation__lt=last_month_first).exclude(
                date_of_resignation__isnull=True)
            separated_employees = Employee.objects.all().exclude(id=1).exclude(
                date_of_separation__gt=last_month_last).exclude(date_of_separation__lt=last_month_first).exclude(
                date_of_separation__isnull=True)
            new_employees = Employee.objects.all().exclude(id=1).exclude(
                date_of_joining__gt=last_month_last).exclude(date_of_joining__lt=last_month_first).exclude(
                date_of_joining__isnull=True)
            form = HeadCountReport({'start_date': last_month_first, 'end_date': last_month_last})
    return render(request, 'emp/head_count_report.html', {'form': form, 'active_employees': active_employees,
                                                          'resigned_employees': resigned_employees,
                                                          'separated_employees': separated_employees,
                                                          'new_employees': new_employees})