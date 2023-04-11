from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserModel(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE,unique=True)
    first_name = models.CharField(max_length=200,null=True,blank=True)
    last_name = models.CharField(max_length=200,null=True,blank=True)
    email = models.CharField(max_length=200,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.first_name
    
class TicketModel(models.Model):
    ticket_number = models.CharField(max_length=200,null=True,blank=True,unique=True)
    first_name = models.CharField(max_length=200,null=True,blank=True)
    last_name = models.CharField(max_length=200,null=True,blank=True)
    phone = models.CharField(max_length=200,null=True,blank=True)
    email = models.CharField(max_length=200,null=True,blank=True)
    payment = models.CharField(max_length=200,null=True,blank=True)
    arrived = models.CharField(max_length=200,null=True,blank=True,default='No')
    qr_code = models.ImageField(null=True, blank=True, upload_to='static/images/tickets')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.first_name
