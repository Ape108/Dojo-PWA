
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class UserType(models.TextChoices):
        STUDENT = 'student', 'Student'
        ADMIN = 'admin', 'Admin'

    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.STUDENT
    )
    is_approved = models.BooleanField(
        default=False,
        help_text='Designates whether an admin has approved this user.'
    )

    @property
    def is_admin(self):
        return self.user_type == self.UserType.ADMIN
    
    @property
    def is_student(self):
        return self.user_type == self.UserType.STUDENT
    