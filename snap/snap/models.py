from django.db import models
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.auth.models import User

# from imagekit.models import ImageSpecField, ProcessedImageField
# from imagekit.processors import ResizeToFill, SmartResize


class Article(models.Model):
    title = models.CharField(max_length=200)
    article_subject=models.CharField(max_length=50,null=True,blank=True)
    summary = models.TextField(null=True,blank=True)
    created_by= models.ForeignKey(User)
    posted_on= models.DateTimeField(auto_now_add=True)
class Comment(models.Model):
    comment = models.CharField(max_length=2500)
    commented_by= models.ForeignKey(User)
    article = models.ForeignKey(Article)
    commented_on = models.DateTimeField(auto_now_add=True)
    
class ExampleModel(models.Model):
    model_pic = models.ImageField(upload_to ='media/',null=True,blank=True)
    
    
class Project(models.Model):
    title = models.CharField(max_length=200)
    project_type=models.CharField(max_length=50,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    proj_pic = models.ImageField(upload_to ='media/projects',null=True,blank=True)
    created_by= models.ForeignKey(User)
    
class UserProfile(models.Model):
    first_name= models.CharField(max_length=200)
    last_name= models.CharField(max_length=200)
    prof_pic= models.ImageField(upload_to ='media/profiles',null=True,blank=True)
    home_address = models.TextField()
    phone_number = models.CharField(max_length=200)
    user = models.ForeignKey(User, unique=True)
    
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save

class UserProfileNew(AbstractUser):
    age = models.PositiveIntegerField(_("age"))
    prof_pic= models.ImageField(upload_to ='media/profiles',null=True,blank=True)
    
def create_user_profile(sender, instance, created, **kwargs):
    """Create the UserProfile when a new User is saved"""
    if created:
        profile = UserProfile()
        profile.user = instance
        profile.save()

post_save.connect(create_user_profile, sender=User)