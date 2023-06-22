from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordResetForm,SetPasswordForm ,PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib import messages


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
      widget = forms.PasswordInput(attrs = {'onkeyup':'checkPassword(this.value)', 'placeholder': 'Enter Password', 'class':'Pwd'}),
      max_length = 50,
      required = True,
      label = 'Passowrd',
   )

   password2 = forms.CharField(
      widget = forms.PasswordInput(attrs = {'placeholder': 'Confrim Password', 'class':'Pwd'}),
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

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control Pwd ', 'placeholder': 'Password'})
    )

    error_messages = {
        'invalid_login': 'Please enter a correct %(username)s and password. Note that both fields may be case-sensitive.',
        'inactive': 'This account is inactive.',
    }


class PwdResetForm(PasswordResetForm):
   email = forms.EmailField(
      widget = forms.TextInput(attrs = {'placeholder': 'Enter Email'}),
      max_length = 30,
      required = True,
      label = 'Email'
   )

   def __init__(self, request=None, *args, **kwargs):
       self.request = request
       super().__init__(*args, **kwargs)

   def clean_email(self):
      email = self.cleaned_data['email']
      check = User.objects.filter(email=email).exists()
      if not check:
         messages.warning(self.request, 'Sorry! we could not find a user with that email address.')
         raise forms.ValidationError('unfortunately we can not find that email address') 
      return email 
   
class PwdResetConfirmForm( SetPasswordForm):
   new_password1 = forms.CharField(
      widget = forms.PasswordInput(attrs = {'onkeyup':'checkPassword(this.value)', 'placeholder': 'Enter Password', 'class':'Pwd' }),
      max_length = 50,
      required = True,
      label = 'Passoword',
   )

   new_password2 = forms.CharField(
      widget = forms.PasswordInput(attrs = {'placeholder': 'Confrim Password', 'class':'Pwd'}),
      max_length = 50,
      required = True,
      label = 'Confirm  Passowrd'
   )


class PwdChangeForm(PasswordChangeForm):
   old_password = forms.CharField(
      widget = forms.PasswordInput(attrs = {'placeholder': 'Old Password', 'class':'Pwd'}),
      max_length = 50,
      required = True,
      label = 'Old Password',
   )

   new_password1 = forms.CharField(
   widget = forms.PasswordInput(attrs = {'placeholder': 'New Password', 'class':'Pwd'}),
   max_length = 50,
   required = True,
   label = 'New Password'
   )

   new_password2 = forms.CharField(
   widget = forms.PasswordInput(attrs = {'placeholder': 'New Password', 'class':'Pwd'}),
   max_length = 50,
   required = True,
   label = 'Confirm  Password'
   )

   def save(self, commit = True):
      user = self.user
      old_password = self.cleaned_data.get('old_password')
      new_password1 = self.cleaned_data.get('new_password1')
      new_password2 = self.cleaned_data.get('new_password2')

      if new_password1 != new_password2:
         messages.warning(self.request, 'New Password and Confirm Password does not match!')
         return

      if user.check_password(old_password):
         user.set_password(new_password1)
         if commit:
            user.save()
            messages.success(self.request, 'Password have been successfully changed.')
      else:
         messages.error(self.request, 'Old password is incorrect!')


class UserProfileUpdateForm(forms.ModelForm):

    username = forms.CharField(
       widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Username'}),
       max_length=15
       )
    
    first_name = forms.CharField(
       widget=forms.TextInput(attrs={'class':'input', 'placeholder':'first_name'}),
        max_length=10
       )
    
    last_name = forms.CharField(
       widget=forms.TextInput(attrs={'class':'input', 'placeholder':'last_name'}),
        max_length=10
       )
    
    email = forms.EmailField(
       widget=forms.EmailInput(attrs={'class':'input','placeholder':'Email'}),
        max_length=25
       )
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
      email = self.cleaned_data['email']
      #check if the email entered in the form is both different from the current email and
      #not already taken by another user.
      if email != self.instance.email and User.objects.filter(email=email).exists():
         messages.warning(self.request, 'Email is already Taken.')
         raise forms.ValidationError('email is already Taken')
      return email

    def clean_username(self):
      username = self.cleaned_data['username']
      if username != self.instance.username and User.objects.filter(username=username).exists():
         messages.warning(self.request, 'Username is already Taken.')
         raise forms.ValidationError('Username is already Taken')
      return username 
    
    class Meta:
         model = User
         fields = ['username', 'first_name', 'last_name', 'email']
    
   

class ProfileUpdateForm(forms.ModelForm):
    
    age = forms.CharField(
       widget=forms.TextInput(attrs={'class':'input', 'placeholder':'age'}),
       max_length=3
       )
    
    image = forms.ImageField(
         widget=forms.FileInput(attrs={'class':'image_input', 'title': 'Choose image' })
    )
    
    class Meta:
       model = Profile
       fields = ['age', 'image']

