from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class tbl_twilioconversation(models.Model):
    sender = models.TextField(default="")
    message = models.TextField(default="")
    response = models.TextField(default="")
    created = models.DateTimeField(default=timezone.now)
    
class tbl_twiliocredentials(models.Model):
    account_sid = models.TextField(default="")
    auth_token = models.TextField(default="")
    number = models.TextField(default="")
    type = models.TextField(default="")
    created = models.DateTimeField(default=timezone.now)
    
class tbl_twiliocontext(models.Model):
    owner = models.TextField(default="")
    context = models.TextField(default="")
    created = models.DateTimeField(default=timezone.now)
    
class tbl_twilioprefix(models.Model):
    owner = models.TextField(default="")
    prefix = models.TextField(default="")
    created = models.DateTimeField(default=timezone.now)
    
class tbl_twiliosuffix(models.Model):
    owner = models.TextField(default="")
    suffix = models.TextField(default="")
    created = models.DateTimeField(default=timezone.now)
    
class tbl_chattemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="acct_sid")
    type = models.TextField(default="")
    content_sid = models.TextField(default="")
    friendly_name = models.TextField(default="")
    language = models.TextField(default="")
    numbers = models.IntegerField(default=0)
    body = models.TextField(default="")
    media_url = models.TextField(default="")
    submit_status = models.TextField(default="")
    created = models.DateTimeField(default=timezone.now)