from django import forms
from .models import Topic,Post,Patients
class Topic_form(forms.ModelForm):
    message=forms.CharField(max_length=4000,widget=forms.Textarea(
        attrs={'rows':'10',"placeholder":"Write Something"}
    ),help_text="max length is 4000")
    class Meta:
        model=Topic
        fields=[
            'subject','message'
        ]
class Post_form(forms.ModelForm):
    class Meta:
        model=Post
        fields=[
            'message'
        ]
class Patient_form(forms.ModelForm):
    class Meta:
        model=Patients
        fields=[
            'name','age','gender','address','visits','visit_date'
        ]