# accounts/management/commands/createsuperadmin.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a super admin user with role="superAdmin"'

    def handle(self, *args, **options):
        User = get_user_model()

        username = input("Username: ")
        email = input("Email: ")
        password = input("Password: ")

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f"User '{username}' already exists."))
            return

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='superAdmin',
            is_staff=True,
            is_superuser=True
        )


        self.stdout.write(self.style.SUCCESS(f"SuperAdmin '{username}' created successfully."))
