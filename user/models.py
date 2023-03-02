from django.db import models
from django.contrib.auth.models import User,AbstractUser

# Create your models here.

class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    profilepic = models.FileField()
    line1 = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    pincode = models.IntegerField()

class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    profilepic = models.FileField()
    line1 = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    pincode = models.IntegerField()
    
class Blog(models.Model):
    bno = models.IntegerField(primary_key=True,default=1)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.FileField()
    category = models.CharField(max_length=100)
    summary = models.TextField(max_length=500)
    content = models.TextField()
    public = models.BooleanField(default=True)
    
    