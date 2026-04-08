from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
    
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ]

    manager = models.ForeignKey('self',on_delete=models.SET_NULL, null=True, blank=True, related_name='team_members',limit_choices_to={'role': 'manager'},)

    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    # manager=models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.username    
    
class attendence(models.Model):
    employee=models.ForeignKey(User, on_delete=models.CASCADE)
    date=models.DateField()
    status=models.CharField(max_length=10,choices=[('present','Present'),('absent','Absent')])

    def __str__(self):
        return f"{self.employee.username}-{self.status}on{self.date}"
    
class leave(models.Model):
    employee=models.ForeignKey(User, on_delete=models.CASCADE)
    start_date=models.DateField()
    end_date=models.DateField()
    reason = models.TextField()
    status=models.CharField(max_length=10,choices=[('pending', 'Pending'),('approved','Approved'),('rejected','Rejected')])
    
    def __str__(self):
        return f"Leave request for {self.employee.username} from {self.start_date} to {self.end_date} - {self.status}"
    

class complaint(models.Model):
    employee=models.ForeignKey(User, on_delete=models.CASCADE)
    complaint_text=models.TextField()
    status=models.CharField(max_length=10, choices=[('pending', 'Pending'),('resolved', 'Resolved')])

    def __str__(self):
        return f"Complaint by {self.employee.username}-{self.status}"