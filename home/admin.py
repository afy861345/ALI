from django.contrib import admin
from .models import Board,Topic,Post,Patients,News
# Register your models here.
admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Patients)
admin.site.register(News)
