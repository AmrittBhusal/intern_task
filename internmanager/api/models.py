from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class UserProfile(User):
    userprofile_choice=(
        ('superviser','superviser'),
        ('intern','intern'),
    )

    role= models.CharField(max_length=10, choices=userprofile_choice)
    
    
class Task(models.Model):
    title=models.CharField(max_length=250)
    assigned_to= models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='task')
    completed=  models.BooleanField(default=True)
    task_given_time = models.DateTimeField(default=timezone.now)
    submitted_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Attendence(models.Model):
    Name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="Attendence")
    date= models.DateField(default=timezone.now)
    Entry_time=models.TimeField()
    Exit_time= models.TimeField()

    def __str__(self):
        return f"{self.Name.username}"