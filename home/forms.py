from django import forms
from .models import Topic
class Topic_form(forms.ModelForm):
    message=forms.CharField(max_length=4000,widget=forms.Textarea(
        attrs={'rows':'10',"placeholder":"Write Something"}
    ),help_text="max length is 4000")
    class Meta:
        model=Topic
        fields=[
            'subject','message'
        ]