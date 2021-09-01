from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.fields.related import ManyToManyField
from django.db.models.query_utils import Q
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import Group, Permission
import uuid 

class User(AbstractUser):
    communities = ManyToManyField('Community', related_name="users")
    
    def get_completed_responses(self):
        return len(QuestionResponse.objects.filter(user=self, is_complete=True))
    
    def get_average_marks(self):
        responses = QuestionResponse.objects.filter(user=self, is_complete=True)
        if not responses:
            return "No questions completed"
        marks = 0
        for response in responses:
            if response.mark:
                marks += response.mark
        average = marks / len(responses)
        return average

class Community(models.Model):
    name = models.CharField(max_length=30)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    date_created = models.DateTimeField(default=timezone.now)
    community_code = models.CharField(default="", max_length=6, unique=True)
    
    class Meta:
        verbose_name_plural = "Communities"
    
    def save(self, *args, **kwargs):
        super(Community, self).save(*args, **kwargs)
        self.users.add(self.admin)
        
    def get_absolute_url(self):
        return reverse('community', kwargs={'pk':self.id})
        
    def __str__(self):
        return self.name
        

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey('community', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    likes = models.BigIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('post', kwargs={'pk':self.id})
    
    def __str__(self):
        return self.content

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey('community', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField()
    date_assigned = models.DateTimeField(default=timezone.now)
    mark = models.IntegerField()
    
    def save(self, *args, **kwargs):
        super(Question, self).save(*args, **kwargs)
        community = Community.objects.get(id=self.community.id)
        all_users = community.users.all()
        objs = []
        for user in all_users:
            user_obj = User.objects.get(id=user.id)
            objs.append(QuestionResponse(user=user_obj, question=self))
        QuestionResponse.objects.bulk_create(objs)
         
    def __str__(self):
        return self.title
    

class QuestionResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    content = models.TextField(null=True)
    time_taken = models.FloatField(null=True)
    mark = models.IntegerField(null=True)
    is_complete = models.BooleanField(default=False)
    
        
    def __str__(self):
        return self.user.username + " | "+ self.question.title



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    likes = models.BigIntegerField(default=0)
    
    def __str__(self):
        return self.content

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.ForeignKey(QuestionResponse,on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.user.username + " | " + self.content
