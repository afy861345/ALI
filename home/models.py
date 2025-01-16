from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from time import strftime
# Create your models here.
class Board(models.Model):
    name =models.CharField(max_length=100,unique=True)
    description=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    def get_posts(self):
        posts=Post.objects.filter(topic__board=self).count()
        return posts
    def get_last_post(self):
        posts=Post.objects.filter(topic__board=self).order_by('created_at').first()
        return posts
class Topic(models.Model):
    subject=models.CharField(max_length=100)
    board=models.ForeignKey(Board,related_name='topics',on_delete=models.CASCADE)
    created_by=models.ForeignKey(User,related_name='topics',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    views=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.subject
class Post(models.Model):
    message=models.TextField(max_length=4000)
    topic=models.ForeignKey(Topic,related_name='posts',on_delete=models.CASCADE)
    created_by=models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_by=models.ForeignKey(User,null=True,related_name='+',on_delete=models.CASCADE)
    updated_at=models.DateTimeField(null=True)
    def __str__(self):
        msg=Truncator(self.message)
        return msg.chars(30)
class Patients(models.Model):
    name=models.CharField(max_length=150,unique=True)
    age=models.IntegerField(null=True)
    gender=models.CharField(max_length=50)
    address=models.CharField(max_length=150,null=True)
    visits=models.PositiveIntegerField(default=0)
    visit_date=models.DateField(default=strftime("%Y-%m-%d"))
    def __str__(self):
        return self.name