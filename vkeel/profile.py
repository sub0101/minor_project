from datetime import date
from django.db.models.base import Model
from django.db.models.fields import NullBooleanField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .manager import UserManager
from .models import *
from django.core.validators import RegexValidator
from django.core.exceptions import ObjectDoesNotExist
import os
from .pythonData import choice



law_choice = choice
gender= [
    ('male', 'male'),
    ('female'  ,'female')
    ]

# Advocate Profile

class CaseProfile(models.Model):
    # user  = models.OneToOneField(User , on_delete=models.CASCADE)
    user = models.ForeignKey(User , related_name='caseprofile', on_delete =models.CASCADE)
    case_title = models.CharField(max_length=150 , default="")
    case_year = models.DateField(  null = True )
    case_law = models.CharField(max_length=50   ,choices = law_choice , default="" )
    case_description  = models.TextField(max_length=1000  ,default="")
    
    

    def __str__(self):
        return  self.user.email


class AdvocateProfile(models.Model):
    
    user = models.OneToOneField(User, related_name='profile' , on_delete=models.CASCADE)

    dob = models.CharField(max_length= 50 , blank=True , default="")
    gender = models.CharField(max_length = 20 , blank=True , default="", null=True)
    state = models.CharField(max_length=30   , default = '', blank=True)
    pincode = models.CharField(max_length=10 , default="", blank=True)
    address = models.TextField(max_length=100 , default="", blank=True  , null=True)
    language_spoken = models.CharField(max_length=200 , blank=True , default="")
    enrollment_number = models.CharField(max_length=100 , blank=True , default=""  , null=True)
    practicing_since = models.CharField(max_length=100, blank=True , default="" )
    bio = models.TextField(max_length=1000, blank=True , default=""  , null=True)
    # mobile=  models.CharField(max_length=10 ,blank = True , unique=True , null=True)

 
    # service_cities  = models.TextField(max_length = 250 ,default = '', blank=True)
    service_cities = models.JSONField(default = list , blank = True ,null = True )

    area_of_law  = models.JSONField(default=list, blank = True , null = True)
    # visiting_courts  = models.CharField(max_length = 250 ,default = '', blank=True)
    visiting_courts = models.JSONField(default = list , blank = True ,null = True )

    def __str__(self):
        return  self.user.email


class EducationModel(models.Model):
    user = models.ForeignKey(User , related_name='educationalprofile',  on_delete=models.CASCADE ,default=None)
    course_name = models.CharField(max_length = 50 , default="" )
    college_name = models.CharField(max_length = 50 , default="")
  
    def __str__(self):
        return self.user.email

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_advocate:
            AdvocateProfile.objects.create(user=instance)
            # CaseProfile.objects.create(user = instance)
            # EducationModel.objects.create(user = instance)
          
            
        else:
            print('created')
            UserProfile.objects.create(user=instance)
       
        

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
  
   
    if instance.is_advocate :

        instance.profile.save()
    elif instance.is_user:
        print('elif')
        instance.userprofile.save()
    else:
        instance.is_user = True
        print('d')
        # print(instance.is_user)
        instance.save()
        print('yes')
        instance.userprofile.save()
    
    

@receiver(models.signals.pre_save, sender=User)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False

    new_file = instance.image
    # if not old_file == new_file:
    #     if os.path.isfile(old_file.path):
    #         os.remove(old_file.path)

    
# -------------------------------------------------------


class UserProfile(models.Model):
    
    user = models.OneToOneField(User, related_name='userprofile' , on_delete=models.CASCADE)  
    dob = models.CharField(max_length=50 , default=None , blank=True ,null=True )
    gender = models.CharField(max_length = 20 , blank=True , default="")
    state = models.CharField(max_length=30   , default = '', blank=True)
    pincode = models.CharField(max_length=10 , default="", blank=True)
    address = models.TextField(max_length=100 , default="", blank=True)
    # mobile=  models.CharField(max_length=10 ,blank = True , unique=True , null=True)

    def __str__(self):
        return  self.user.email


