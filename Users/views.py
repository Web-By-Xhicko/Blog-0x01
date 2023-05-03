from django.shortcuts import redirect, render
from django.contrib.auth import authenticate , login, logout
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib import messages
from django.utils.safestring import mark_safe


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