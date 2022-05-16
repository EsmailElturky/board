from dataclasses import fields
from pyexpat import model
from django import forms
from .models import Post, Topic

class NewTopicForm(forms.ModelForm):

    message = forms.CharField(widget=forms.Textarea(attrs={'row':5,'placeholder':'what is in your mind'}),max_length=4000
    ,help_text='max length is 4000')

    class Meta:
        model=Topic
        fields=['subject','message']

class Postform(forms.ModelForm):
    class Meta:
        model=Post
        fields=['message']

