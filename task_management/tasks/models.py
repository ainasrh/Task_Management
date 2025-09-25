from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    ROLE_CHOICES = [
        ("superadmin","SuperAdmin"),
        ("admin","Admin"),
        ("user","User")
    ]

    role = models.CharField(max_length=100,choices=ROLE_CHOICES,default="user")
    assigned_to= models.ForeignKey("self",null=True,blank=True,on_delete=models.SET_NULL,limit_choices_to={'role':"admin"})



    @property
    def is_superadmin(self):
        return self.role == "superadmin"
    


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    completion_report = models.TextField(blank=True, null=True)
    worked_hours = models.PositiveIntegerField(blank=True, null=True)



