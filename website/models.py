from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import uuid
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile

# Create your models here.
class UserDetails(models.Model):
    name = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    is_doctor = models.BooleanField(default=False)
    
    is_first_login = models.BooleanField(default=True)

    def __str__(self):
        return "Name : " + self.name + "    " + self.user.username + "    " + str(self.is_doctor) 



class DoctorDetails(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dp = models.ImageField(upload_to='photo/', default='/dp.jpg')
    phone = models.CharField(max_length=10, null= True, default='', blank=True)
    gender = models.CharField(max_length=10, null=True,default='', blank=True)
    about = models.TextField(null = True, blank=True,default='')
    clinic_name = models.CharField(max_length=256, null = True, blank=True)
    price = models.CharField(max_length=25,null = True,default='', blank=True)
    Specialization = models.CharField(max_length=256,default='', null = True, blank=True)
    is_verified = models.BooleanField(default=False)
    mark = models.BooleanField(default = False)
    degree = models.ImageField(upload_to ='uploads/', blank=True, null=True)
    degree_name = models.CharField(max_length=30, default="Doctor")
    services = models.CharField(max_length=256, default="")
    state = models.CharField(max_length=256, default='', null=True, blank=True)
    country = models.CharField(max_length=256, default='', null=True, blank=True)


    


class Work(models.Model):
    id = models.AutoField(primary_key=True)
    hospital = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.CharField(max_length=256, default = '')
    start = models.CharField(max_length = 256)
    end = models.CharField(max_length = 256)

class Slot(models.Model):
    id = models.AutoField(primary_key=True)
    docId = models.ForeignKey(DoctorDetails, on_delete=models.CASCADE)
    patientId = models.ForeignKey(User, on_delete = models.CASCADE)
    slot = models.CharField(max_length=256)
    date = models.DateField()
    startUrl = models.URLField(max_length=256, default="https://google.com")
    meetUrl = models.URLField(max_length=256, default="https://google.com")

class Zoom(models.Model):
    id = models.AutoField(primary_key=True)
    access_token = models.CharField(default = '', null=True, blank = True, max_length=1000)
    token_type = models.CharField(default = '', max_length=1000)
    refresh_token = models.CharField(default='', max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expires = models.DateTimeField()
    scope = models.CharField(default='', max_length=1000)

class PatientDetails(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userD = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    state = models.CharField(max_length=256, default='')
    country = models.CharField(max_length=256, default='')
    phone = models.CharField(max_length=256, default='')
    dp = models.ImageField(upload_to='patients/photos/',default='dp.jpg',blank=True, null=True)

class allPatients(models.Model):
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientDetails, on_delete=models.CASCADE)