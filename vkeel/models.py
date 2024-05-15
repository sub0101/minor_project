from __future__ import unicode_literals

from datetime import datetime, timedelta
from django.db import models
import uuid


from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models.base import ModelState
from django.utils.translation import deactivate, ugettext_lazy as _
from .manager import UserManager
from django.utils.timezone import now
from vkeel.pythonData import choice
from cloudinary.models import CloudinaryField
# choice = (
 
#     ("Property Law", "Property Law"), 
#     ("Environmental Law", "Environmental Law"), 
#     ("Civil Law", "Civil Law"), 
#     ("Cyber Law", "Cyber Law"), 
# )

class User(AbstractBaseUser, PermissionsMixin):
    
    is_advocate = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    image =CloudinaryField("image" )
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('name'), max_length=30, blank=True)
    city = models.CharField(max_length = 30  , blank = True , null=True)
    mobile=  models.CharField(max_length=10 ,blank = True , unique=True , null=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        name = '%s' % (self.name)
        return name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Question(models.Model):
    user = models.ForeignKey(User ,default= None, on_delete= models.CASCADE)
    title = models.CharField(max_length=200 , blank=True , default="")
    question_description = models.TextField(max_length=1000 , blank=True , default="")
    area_of_law   = models.CharField(max_length = 100 ,choices = choice , default = '1', blank=True)
    date_posted = models.DateTimeField(null=True)
   
    def __str__(self):
        return  str(self.title)

class Answer(models.Model):
    question = models.ForeignKey(Question , on_delete=models.CASCADE)
    user = models.ForeignKey(User ,on_delete= models.CASCADE )
  
    reply = models.TextField(max_length=2000 , null=True)
    
   
    def __str__(self):
        return  str(self.question.title)

class Rating(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    reviewer = models.CharField(max_length=100 , default="" )
    rate = models.IntegerField(null=True , default=0)
    post =models.TextField(max_length=500 , default="")
    

    def __str__(self):
        return self.user.email


class InstantAdvice(models.Model):

    user = models.ForeignKey(User , max_length=200 , blank=True, on_delete = models.CASCADE)
    name = models.CharField(max_length=20 , default="")
    ammount = models.IntegerField(blank=True, default=0)
    created = models.DateTimeField(auto_now_add=True)
    mobile = models.IntegerField(default=0)
    advocate=models.EmailField(blank=False)
    transaction_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)

    def __str__(self):
        return self.user.name


class ContactUs(models.Model):

    name = models.CharField(max_length=20 , default="")
    email = models.EmailField()
    mobile = models.IntegerField(default=0)
    query = models.TextField(max_length=500)
    date = models.DateTimeField(null=True, auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.email)

class Follower(models.Model):

    follower = models.ForeignKey("User",on_delete=models.CASCADE, related_name= "follower")
    following = models.ForeignKey("User" , on_delete=models.CASCADE, related_name="following")

    date =models.DateTimeField(auto_now_add=True)


class ActiveChat(models.Model):
    chat_user = models.ForeignKey("User" ,on_delete=models.CASCADE , related_name="chat_user" )
    
    chat_user2 = models.ForeignKey('User' , on_delete=models.CASCADE , related_name="chat_user2")
    date = models.DateField(auto_now_add=True)