from django.shortcuts import redirect, render
from django.contrib.auth import authenticate , login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserLoginForm, PwdResetForm, PwdChangeForm
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required

def Register(request):
    if request.method == 'POST':
         form = UserRegistrationForm(request.POST)
         if form.is_valid():
             form.save()
             username = form.cleaned_data.get('username')
             messages.success(request, mark_safe( f'Account Sucessfully created for {username}! &nbsp; Welcome to Infohub!'))
             return redirect('Login_Page')
    else:
        form = UserRegistrationForm()
    return render(request, 'Users/Register.html', {'form': form})


def Login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, mark_safe( f'Hello {username}, You logged In Successfully'))
            return redirect('blogApp:Home_Page')
        else:
            messages.error(request, 'Invalid Username Or Password.')
    else:
        form = UserLoginForm()
    return render(request, 'Users/Login.html',{'form': form})


def Logout(request):
    logout(request)
    messages.warning(request,'You have Logged out Sucessfully, Login Again?' )
    return redirect('Login_Page')


class PasswordResetFormPage(PasswordResetView):
    form_class = PwdResetForm
    template_name = 'Users/Password_Reset.html'
    email_template_name = 'Users/Password_Reset_Email.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)
        current_site = get_current_site(self.request)
        subject = 'Reset Your Password'
        message = render_to_string('Users/Password_Reset_Email.html', {
            'user': user,
            'domain' : current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        user.email_user(subject=subject, message=message) 
        return super().form_valid(form)
    

class PassowrdResetDonePage(PasswordResetFormPage):
    template_name = 'Users/Password_Reset.html'
   
    def get_success_url(self):
        return reverse_lazy('Password_Reset_Page')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Verification successful! check your email for the password reset link.')
        return super().get(request, *args, **kwargs)
    