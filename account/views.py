from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from.forms import User_form
# Create your views here.
def index(request):
    return HttpResponse("<h1>Hello Ali</h1>")
def logout(request):
    auth_logout(request)
    return redirect('main')
def signup(request):
    if request.method=="POST":
        form=(request.POST)
        form=User_form(request.POST)
        # form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            auth_login(request,user)
            return redirect('main')
    else:
        form=User_form()
    return render(request,"account/signup.html",{'form':form})
