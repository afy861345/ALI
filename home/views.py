from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return HttpResponse("<h1>Hello Ali</h1>")
def main(request):
    return render(request,'home/main.html')