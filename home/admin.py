from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Board,Topic,Post,Patients,News,Visit,Photo
from import_export.admin import ImportExportModelAdmin
# Register your models here.
admin.site.site_header="Ali Clinic"
admin.site.site_title="Ali Clinic"
admin.site.unregister(Group)
admin.site.register(Post)
admin.site.register(Patients)
admin.site.register(News)
admin.site.register(Visit)
admin.site.register(Photo)
#classes
class Topic_admin(ImportExportModelAdmin):#or normal(admin.ModelAdmin)
    fields=['subject','board','created_by']
    list_display=['subject','board','created_by','compined']#not call by self
    list_display_links=['board','created_by']
    list_editable=['subject']
    search_fields=['board','created_by']
    list_filter=['board']
    def compined(self,obj):
        return f"{obj.subject}-{obj.board}"
admin.site.register(Topic,Topic_admin)
class Inlined_toipc(admin.TabularInline):#admin.StackedInline
    model=Topic
    extra=1#make 1 table
class Board_admin(admin.ModelAdmin):
    inlines=[Inlined_toipc]
  
admin.site.register(Board,Board_admin)