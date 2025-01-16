from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from.forms import User_form
from django.urls import reverse_lazy
from django.views.generic import UpdateView
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

#user
class Update_user(UpdateView):
    model=User
    fields=['first_name','last_name','email']
    success_url=reverse_lazy("my_account")
    template_name="account/my_account.html"
    def get_object(self):
        return self.request.user