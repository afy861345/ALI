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
    updated_by=models.ForeignKey(User,null=True,related_name='+',on_delete=models.CASCADE)
    updated_at=models.DateTimeField(null=True)
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
    visit_date=models.DateField(default=strftime("%Y-%m-%d"),null=True)
    def __str__(self):
        return self.name
class Visit(models.Model):
    date=models.DateField(default=strftime("%Y-%m-%d"))
    patient=models.ManyToManyField(Patients,related_name='visit')
class News(models.Model):
    name=models.CharField(max_length=150)
    content=models.TextField(max_length=4000,null=True)
    created_by=models.ForeignKey(User,related_name='news',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)   
    def __str__(self):
        return self.name
class Photo(models.Model):
    images=models.ImageField(upload_to="photos/%Y/%m/%d",null=True)
    file=models.FileField(upload_to='pdfs/%Y/%m/%d',null=True)
    patient=models.ForeignKey(Patients,related_name='files',on_delete=models.CASCADE)
    visit=models.ForeignKey(Visit,related_name='files',null=True,on_delete=models.CASCADE)
    add_at=models.DateField(default=strftime("%Y-%m-%d"))