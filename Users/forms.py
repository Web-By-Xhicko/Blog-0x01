from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password


class UserRegistrationForm(UserCreationForm):
   username = forms.CharField(
      widget= forms.TextInput(attrs = {'placeholder':'Enter Username'}),
      max_length = 30,
      required = True,
      label = 'Username' 
   )

   email = forms.EmailField(
      widget = forms.TextInput(attrs = {'placeholder': 'Enter Email'}),
      max_length = 30,
      required = True,
      label = 'Email'
   )

   password1 = forms.CharField(
      widget = forms.PasswordInput(attrs = {'placeholder': 'Enter Password'}),
      max_length = 50,
      required = True,
      label = 'Passowrd',
      help_text = 'Your password can not be too similar to your other personal information. <br> Your password must contain at least 8 characters.<br> Your password can not be a commonly used password.<br> Your password can not  be entirely numeric <br>'
   )

   password2 = forms.CharField(
      widget = forms.PasswordInput(attrs = {'placeholder': 'Confrim Password'}),
      max_length = 50,
      required = True,
      label = 'Confirm  Passowrd'
   )

   class Meta:
      model = User
      fields = ['username', 'email', 'password1', 'password2']
      exclude = ['help_text']

   def clean_username(self):
      username = self.cleaned_data['username']
      if User.objects.filter(username=username).exists():
         raise forms.ValidationError('Username is already Taken')
      return username
   
   def clean_email(self):
      email = self.cleaned_data['email']
      if User.objects.filter(email = email).exists():
         raise forms.ValidationError('Email is Already Taken')
      return email
   
   def clean(self):
      cleaned_data = super().clean()
      password1 = cleaned_data.get('password1')
      password2 = cleaned_data.get('password2')
      if password1 and password2 and password1 != password2:
         raise ValidationError('Passwords does not match')
      return cleaned_data
   
   def encryptPassword(self):
      password = make_password(self.cleaned_data['password1'])
      user = User.objects.create(
         username = self.cleaned_data['username'],
         email = self.cleaned_data['email'],
         password = password,
      )

      return user