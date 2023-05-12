from audioop import reverse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate , login, logout
from .forms import UserRegistrationForm, UserLoginForm, PwdResetForm
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.contrib.auth.views import PasswordResetView
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


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
            messages.success(request, mark_safe( f'Hello {username}...You are now logged in, Enjoy your Time!'))
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    # def form_valid(self, form):
    #     # Generate a one-time use token and send the password reset email
    #     uidb64 = urlsafe_base64_encode(force_bytes(form.cleaned_data['email']))
    #     token = default_token_generator.make_token(form.user_cache)
    #     reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
    #     reset_url = self.request.build_absolute_uri(reset_url)
    #     context = {
    #         'user': form.user_cache,
    #         'protocol': self.request.scheme,
    #         'domain': self.request.get_host(),
    #         'reset_url': reset_url,
    #     }
    #     message = render_to_string(self.email_template_name, context=context)