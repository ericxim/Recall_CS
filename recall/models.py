from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.fields.related import ManyToManyField
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import Group, Permission
import uuid 

class User(AbstractUser):
    communities = ManyToManyField('Community', related_name="user_communities")

class Community(Group):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    date_created = models.DateTimeField(default=timezone.now)
    community_code = models.CharField(default=uuid.uuid4().hex[:6].upper(), max_length=6)
    
    class Meta:
        verbose_name_plural = "Communities"
    
    def __str__(self):
        return self.name
        

class Post(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    community_id = models.ForeignKey('community', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    likes = models.BigIntegerField(default=0)
    
    def __str__(self):
        return self.content

class Question(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    community_id = models.ForeignKey('community', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField()
    date_assigned = models.DateTimeField(default=timezone.now)
    mark = models.IntegerField()
    
    def __str__(self):
        return self.title
    
class QuestionResponse(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.ForeignKey('Question', models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    time_taken = models.FloatField()
    mark = models.IntegerField(null=True)
    
    def __str__(self):
        return self.user_id

class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    likes = models.BigIntegerField(default=0)
    
    def __str__(self):
        return self.content