from dataclasses import field
from importlib.metadata import files
from pyexpat import model
from turtle import textinput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.forms import ModelForm
from django.forms.widgets import TextInput



class userCreationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email']

class user_loginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()    

class profileCreationForm(ModelForm):
    class Meta:
        model = userProfile
        fields = ['userImage','is_student']
class examsCreationForm(ModelForm):
    class Meta:
        model = Exam
        fields = ['title']

    

class questionCreationForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        exclude = ['exam','questionId']
        widgets = {
            'examId':TextInput(attrs={'readonly':'true'}),
            'questionId':TextInput(attrs={'readonly':'true'})
        }
    
class answerCreationForm(ModelForm):
    class Meta:
        model = answeredQuestion
        fields = '__all__'

class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)
    