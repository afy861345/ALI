from django.contrib import admin
from .models import Board,Topic,Post,Patients,News,Visit,Photo
# Register your models here.
admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Patients)
admin.site.register(News)
admin.site.register(Visit)
admin.site.register(Photo)
