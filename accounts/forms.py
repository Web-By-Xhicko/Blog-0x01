from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm

class PasswordResetConfirmForm(SetPasswordForm):
    new_passwordOne = forms.CharField(
        label='New Password', widget=forms.PasswordInput(
            attrs={'class':'input', 'placeholder':'Enter Password', 'id':"Password"}
        ))
    
    new_passwordTwo = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput(
            attrs={'class':'input', 'placeholder':'Enter Password', 'id':"Password"}
        ))


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=260, widget=forms.TextInput(
        attrs={'class':'input', 'placeholder':'Email',}
    ))

    def clean_email(self):
        #checking to see if the email exist in the database
        email = self.cleaned_data['email']
        test = User.objects.filter(email=email)
        #if it does not exist 
        if not test:
            raise forms.ValidationError('Email does not exist')
        return email
    
    

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class':'input', 
               'id': 'Username',
               'placeholder':'Username',}
        ))
    
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={ 'class':'input', 
               'id': 'Username_p',
               'placeholder':'Password'}
        ))
    
    class Meta:
        model = User
        fields = ('username', 'password')
    
    def __init__(self, *args, **kwargs):
        print("Initializing UserLoginForm")
        super().__init__(*args, **kwargs)
    



class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label='Enter Username', min_length=5, max_length=50, help_text='Required'
    )

    email = forms.EmailField(
        label='Enter E-mail', max_length=100, help_text='Required', error_messages={
        'required': 'sorry, you will need an email'
        })
    
    password = forms.CharField(
        label='Enter Password', widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput
    )

    class Meta:
        model = User 
        fields = ('username', 'email', 'first_name',)
    #checking to see if user email exist in the database
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError('Username Already Exist!')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('E-Mail Already exist!')
        return email

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password Does Not Match!')
        return cd['password2']

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update(
            {'class':'input', 'placeholder':'Username'}
        )

        self.fields['email'].widget.attrs.update(
            {'class':'input', 'placeholder':'E-Mail'}
        )

        self.fields['password'].widget.attrs.update(
            {'class':'input', 'placeholder':'Enter Password'}
        )

        self.fields['password2'].widget.attrs.update(
            {'class':'input', 'placeholder':'Confirm Password'}
        )
