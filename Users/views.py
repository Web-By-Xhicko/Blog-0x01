from audioop import reverse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate , login, logout
import Users
from .forms import UserRegistrationForm, UserLoginForm, PwdResetForm, PwdResetConfirmForm
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.utils.http import  urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes,  force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site

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

class PassowrdResetDonePage(PasswordResetFormPage):
    template_name = 'Users/Password_Reset.html'
   
    def get_success_url(self):
        return reverse_lazy('Password_Reset_Page')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Verification successful! check your email for the password reset link.')
        return super().get(request, *args, **kwargs)
    
    
class PasswordResetConfirmView(PasswordResetConfirmView):
    form_class = PwdResetConfirmForm
    template_name = 'Users/Password_Reset_Confirm.html'

    
    def get(self, request, uidb64=None, token=None, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Users.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            current_site = get_current_site(request)
            context = {
                'form': self.form_class(user=user),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'current_site': current_site,
            }
            return render(request, self.template_name, context)
        else:
            messages.error(request, 'The link you entered is either  invalid or expired')
            return redirect('Password_Reset_Page')
        
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been reset.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the error below.')
        return super().form_invalid(form)

    # def get_success_url(self):
    #     return reverse_lazy('password_reset_complete')



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