from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from django.urls import reverse


class User(AbstractUser):
    pass

class Post(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    community_id = models.ForeignKey('Community', models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=30)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    likes = models.BigIntegerField(default=0)
    def __str__(self):
        return self.content

class Question(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    community_id = models.ForeignKey('Community', models.SET_NULL, null=True, blank=True)
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


class CommunityMember(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    community_id = community_id = models.ForeignKey('Community', models.SET_NULL, null=True, blank=True)
    
class Community(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    community_code = models.CharField(max_length=5)
    date_created = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name

class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    likes = models.BigIntegerField(default=0)
    def __str__(self):
        return self.content