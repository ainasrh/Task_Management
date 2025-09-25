from django.urls import path
from .user.user_views import RegisterApi, LoginAPi, UserProfileApi
from .task_views import TaskListApi, TaskUpdateApi
from .admin_views import (
    view_users,
    create_user,
    delete_user,
    assign_role,
    assign_admin,
    all_task,
    create_task,
    superadmin_edit_task,
    completed_tasks,
    dashboard,
    login_view,
    logout_view,
    admin_dashboard,
    admin_create_task,
    admin_edit_task,
    no_access,
)

urlpatterns = [
    

    path("register/", RegisterApi.as_view(), name="register"),
    path("login/", LoginAPi.as_view(), name="login"),
    path("profile/", UserProfileApi.as_view(), name="profile"),

    # tasksAPI

   
    path('list-task/', TaskListApi.as_view(), name='list-task'),
    path('update-task/<int:pk>/', TaskUpdateApi.as_view(), name='update-task'),

  

    path('no-access/', no_access, name='no_access'),
    # SuperAdmin URLs
    path('user/<str:role>/', view_users, name="all-users"),
    path('create-user/', create_user, name='create-user'),
    path('delete-user/<int:id>/', delete_user, name='delete-user'),
    path('assign-role/<int:user_id>/', assign_role, name='assign-role'),
    path('assign-admin/<int:user_id>/', assign_admin, name='assign-admin'),
    path('all-task/', all_task, name='all-task'),
    path('create-task/', create_task, name='create-task'),
    path('edit-task/<int:task_id>/', superadmin_edit_task, name='superadmin-edit-task'),
    path('completed-tasks/', completed_tasks, name='completed-tasks'),
    path('superadmin-dashboard/', dashboard, name='superadmin_dashboard'),
    path('auth/login/', login_view, name='admin-login'),
    path('auth/logout/', logout_view, name='admin-logout'),

    # Admin URLs
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/create-task/', admin_create_task, name='admin-create-task'),
    path('admin/edit-task/<int:task_id>/', admin_edit_task, name='admin-edit-task'),

]