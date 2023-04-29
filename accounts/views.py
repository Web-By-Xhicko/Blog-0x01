from django.shortcuts import render,  redirect
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm , UserLoginForm
from .token import account_activation_token
# from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


@login_required
def account_profile(request):
    return render(request,
                  'accounts/profile.html',
                  {'section':'profile'})


# def account_creation_message(request):
#     return render(request,'accounts/account_creation_message.html',)

# def login_view(request):
#     if request.method == 'POST':
#         login_form = UserLoginForm(request.POST)
#         if login_form.is_valid():
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None and user.is_active:
#                 login(request, user)
#                 return redirect('account_profile')
#             else:
#                 error_message = "Invalid login credentials or account not activated"
#                 return render(request, 'registration/login.html', {'error_message': error_message, 'form': login_form})
#     else:
#         login_form = UserLoginForm()
#     # Return a response object here that gets returned when request.method is not 'POST'
#     return render(request, 'registration/login.html', {'form': login_form})



def account_registration(request):
    #if the request the user is making is a post request
    if request.method == 'POST':
        #Captures the registration form details into the registerform variable
        registerForm = RegistrationForm(request.POST)
        #if the form is valid
        if registerForm.is_valid():
            #capturs all the details in the form but dont send to the database yet
            user = registerForm.save(commit=False)
            #save the specific information 
            user.username = registerForm.cleaned_data['username']
            #save the specific information 
            user.email = registerForm.cleaned_data['email']
             #save the specific information 
            # user.make_password(registerForm.cleaned_data['password'])
            user.password = make_password(registerForm.cleaned_data['password'])
            #user cant be able to login just yet even after creating an account
            user.is_active = False
            #save all information into the database
            user.save()
            #gets a sites information
            current_site = get_current_site(request)

            subject = 'Activate Your Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return render(request, 'accounts/account_creation_message.html', )
    else:
        registerForm = RegistrationForm()
    return render(request, 'registration/register.html', {'form':registerForm})


# def login(request):
#     if request.method == 'POST':
#         loginForm = UserLoginForm(request.POST)
#          # Get the user's credentials from the POST data
#         username = request.POST['username']
#         password = request.POST['password']
#          # Authenticate the user using Django's built-in authentication system
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('Profile_Page')
#         else:
#             return render(request, 'registration/login.html',  {'error_message':'Invalid username or password.'})

#     else:
#         # If the request is not a POST request, show the login form
#         return render(request, 'registration/login.html')

    


def activate(request, uidb64, token):
    try:
        #captures the user id and decodes it
        uid = force_str(urlsafe_base64_decode(uidb64))
        #user id , to know which account is being activated
        user = User.objects.get(pk=uid)
        #if the email link from the email is incorrect it will send an error 
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        #if everything goes fine 
    if user is not None and account_activation_token.check_token(user, token):
        #sets the user active to yes so they can now log in
        user.is_active = True
        #save the active state to the database of the current user
        user.save()
        # Set the user's backend to the default Django backend
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        #login the user
        login(request, user)
        return redirect('login')
    else:
        return render(request, 'registration/activation_invalid.html')