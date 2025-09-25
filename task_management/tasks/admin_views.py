from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout







def no_access(request):
    return render(request, 'no_acces.html')


@login_required

def view_users(request,role):
    if request.user.role != 'superadmin':
        return redirect('no_access')
    users = User.objects.filter(role=role)
    admins=User.objects.filter(role="admin")
    title=role
    return render(request, 'superadmin/viewAllUsers.html', {'users': users,"admins":admins,"title":role})



@login_required

def create_user(request):
    if request.user.role != 'superadmin':
        return redirect('no_access')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        role =request.POST.get('role')
        password = request.POST.get('password')
        password2=request.POST.get('password2')


        if password != password2:
            messages.error(request,"password does not match")
            
        # Basic validation
        if not username or not password:
            messages.error(request, "Username and password are required.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            # Create and save the user
            user = User(
                username=username,
                email=email,
                role=role,
                password=make_password(password)
            )

            user.save()
            return redirect('all-users',role='user')
    return render(request,'superadmin/createUser.html',{'title': 'Create User'})

@login_required
def delete_user(request,id):
    if request.user.role != 'superadmin':
        return redirect('no_access')
    user = get_object_or_404(User,id=id)
    if user.role != 'superadmin':
        user.delete()
    return redirect('all-users',role='user')

@login_required

def assign_role(request, user_id):
    if request.user.role != 'superadmin':
        return redirect('no_access')
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        new_role = request.POST['role']
        user.role = new_role
        user.save()
        redirect_role = 'user' if new_role == 'admin' else 'admin'
        return redirect('all-users', role=redirect_role)
    return redirect('all-users',role='user')

@login_required

def assign_admin(request, user_id):
    if request.user.role != 'superadmin':
        return redirect('no_access')
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        admin_id = request.POST.get('assigned_to')
        if admin_id:
            admin_user = get_object_or_404(User, id=admin_id, role='admin')
            user.assigned_to = admin_user
            user.save()
    return redirect('all-users', role=user.role)


# TASKS-------------
@login_required
def all_task(request):
    if request.user.role != 'superadmin':
        return redirect('no_access')
    tasks=Task.objects.all()
    return render(request,'superadmin/listAllTasks.html',{'tasks':tasks})


# Create Task



# @login_required

def create_task(request):
    if request.user.role != 'superadmin':
        return redirect('no_access')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to_id = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')
        status = request.POST.get('status')

        if not (title and description and assigned_to_id and due_date and status):
            messages.error(request, "Please fill in all required fields.")
            return redirect('create-task')

        try:
            assigned_to = User.objects.get(id=assigned_to_id, role='user')
        except User.DoesNotExist:
            messages.error(request, "Invalid user selected.")
            return redirect('create-task')


        Task.objects.create(
            title=title,
            description=description,
            assigned_to=assigned_to,
            due_date=due_date,
            status=status,
        )
        messages.success(request, "Task created successfully!")
        return redirect('all-task')  

    else:
        users = User.objects.filter(role='user')
        status_choices = Task.STATUS_CHOICES
        return render(request, 'superadmin/createTask.html', {'users': users, 'status_choices': status_choices})



@login_required

def superadmin_edit_task(request, task_id):
    if request.user.role != 'superadmin':
        return redirect('no_access')
    task = Task.objects.get(id=task_id)
    users = User.objects.filter(role='user')
    status_choices = Task.STATUS_CHOICES

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to_id = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')
        status = request.POST.get('status')
        completion_report = request.POST.get('completion_report')
        worked_hours = request.POST.get('worked_hours')

        if not (title and description and assigned_to_id and due_date and status):
            messages.error(request, "Please fill in all required fields.")
            return redirect('superadmin-edit-task', task_id=task_id)

        try:
            assigned_to = User.objects.get(id=assigned_to_id, role='user')
        except User.DoesNotExist:
            messages.error(request, "Invalid user selected.")
            return redirect('superadmin-edit-task', task_id=task_id)


        task.title = title
        task.description = description
        task.assigned_to = assigned_to
        task.due_date = due_date
        task.status = status
        task.completion_report = completion_report
        task.worked_hours = worked_hours
        task.save()

        messages.success(request, "Task updated successfully!")
        return redirect('all-task')

    return render(request, 'superadmin/editTask.html', {
        'task': task,
        'users': users,
        'status_choices': status_choices
    })


@login_required

def completed_tasks(request):
    if request.user.role != 'superadmin':
        return redirect('no_access')
    tasks = Task.objects.filter(status='completed')
    return render(request, 'superadmin/completedTask.html', {'tasks': tasks})

@login_required

def dashboard(request):
    if request.user.role != 'superadmin':
        return redirect('no_access')

    completed_tasks_count = Task.objects.filter(status='completed').count()

    admin_users_count = User.objects.filter(is_staff=True).count()

    regular_users_count = User.objects.filter(is_staff=False).count()

    all_task_count=Task.objects.all().count()

    context = {
        'completed_tasks_count': completed_tasks_count,
        'admin_users_count': admin_users_count,
        'regular_users_count': regular_users_count,
        'all_task':all_task_count
    }

    return render(request, 'superadmin/superadmin_dashboard.html', context)




# LOGIN



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.role in ['admin', 'superadmin']:
                login(request, user)
        
                if user.role == 'admin':
                    return redirect('admin_dashboard')  
                else:
                    return redirect('superadmin_dashboard')  
            else:
                messages.error(request, "You don't have permission to access this area.")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request,'auth/Login.html')


def logout_view(request):
    logout(request)
    return redirect('admin-login')


# ADMIN -------


from django.contrib.auth.decorators import login_required
from .models import User, Task


@login_required
def admin_dashboard(request):
    admin_user = request.user

    
    if admin_user.role != 'admin':
        return render(request, 'Admin/not_authorized.html')  

    
    assigned_users = User.objects.filter(assigned_to=admin_user)


    tasks = Task.objects.filter(assigned_to__in=assigned_users)

    return render(request, 'Admin/admin_Dashboard.html', {
        'assigned_users': assigned_users,
        'tasks': tasks
    })


@login_required
def admin_create_task(request):
    if request.user.role != 'admin':
        return redirect('no_access')

    assigned_users = User.objects.filter(assigned_to=request.user)

    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to_id = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')
        status = request.POST.get('status')
        completion_report = request.POST.get('completion_report')
        worked_hours = request.POST.get('worked_hours')

        
        try:
            assigned_to_user = assigned_users.get(id=assigned_to_id)
        except User.DoesNotExist:
            return render(request, 'Admin/admin_create_task.html', {'assigned_users': assigned_users, 'error': 'Invalid user selected.'})

        
        Task.objects.create(
            title=title,
            description=description,
            assigned_to=assigned_to_user,
            due_date=due_date,
            status=status,
            completion_report=completion_report,
            worked_hours=worked_hours or None
        )
        return redirect('admin_dashboard')

    return render(request, 'Admin/admin_create_task.html', {'assigned_users': assigned_users})





@login_required
def admin_edit_task(request, task_id):
    if request.user.role != 'admin':
        return redirect('no_access')

    task = get_object_or_404(Task, id=task_id)
    assigned_users = User.objects.filter(assigned_to=request.user)

    if task.assigned_to not in assigned_users:
        return redirect('no_access')

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        assigned_to_id = request.POST.get('assigned_to')
        task.due_date = request.POST.get('due_date')
        task.status = request.POST.get('status')
        task.completion_report = request.POST.get('completion_report')
        task.worked_hours = request.POST.get('worked_hours') or None

   
        try:
            task.assigned_to = assigned_users.get(id=assigned_to_id)
            task.save()
            return redirect('admin_dashboard')
        except User.DoesNotExist:
            return render(request, 'Admin/edit_task.html', {
                'task': task,
                'assigned_users': assigned_users,
                'error': 'Invalid assigned user selected.'
            })

    return render(request, 'Admin/Admin_edit_task.html', {
        'task': task,
        'assigned_users': assigned_users
    })



