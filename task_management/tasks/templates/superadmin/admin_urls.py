from django.urls import path
from .admin_views import *

urlpatterns =[

     path('no-access/', no_access, name='no_access'),
        #Super Admin ----------

    path('user/<str:role>/',view_users,name="all-users"),
    path('createuser/',create_user,name='create-user'),
    path('deleteuser/<int:id>/',delete_user,name='delete-user'),
    path('assign-role/<int:user_id>/',assign_role, name='assign_role'),
    path('superadmin/assign-admin/<int:user_id>/', assign_admin, name='assign_admin'),
    path('alltasks/',all_task,name='all-task'),
    path('createtask/', create_task, name='create-task'),
    path('edit-task/<int:task_id>',edit_task,name='edit-task'),
    path('completed-task/',completed_tasks,name='completed-task'),
    path('superadmin-dashboard/',dashboard,name='superadmin_dashboard'),

    # Admin URL  ---------

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin_task_edit/<int:task_id>/', edit_task, name='edit_task'),
    path('admin-create-task/',admin_create_task,name='admin-create-task')

]