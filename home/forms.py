from django import forms
from .models import Topic,Post,Patients,News,Visit,Photo
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
class Visit_form(forms.ModelForm):
    date=forms.DateField(widget=forms.DateInput())
    image=forms.ImageField(widget=forms.FileInput(),required=False)
    file=forms.FileField(widget=forms.FileInput(),required=False)
    
    class Meta:
        model=Visit
        fields=[
            'date','file','image'
        ]
class Media_form(forms.ModelForm):
    images=forms.ImageField(widget=forms.FileInput(),required=False)
    file=forms.FileField(widget=forms.FileInput(),required=False)
    class Meta:
        model=Photo
        fields=[
            'images','file','add_at'
        ]
class News_form(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':"write title",}
    ))
    content=forms.CharField(widget=forms.Textarea(
        attrs={'placeholder':"write content","rows":"5"}
    ))
    class Meta:
        model=News
        fields=['name','content']