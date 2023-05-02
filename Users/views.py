from django.shortcuts import redirect, render
from django.contrib.auth import authenticate , login
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib import messages
from django.utils.safestring import mark_safe


def Register(request):
    if request.method == 'POST':
         form = UserRegistrationForm(request.POST)
         if form.is_valid():
             form.save()
             username = form.cleaned_data.get('username')
             messages.success(request, mark_safe( f'Account Sucessfully created for {username}! &nbsp; &nbsp; Welcome to Infohub!'))
             return redirect('Login_Page')
    else:
        form = UserRegistrationForm()
    return render(request, 'Users/Register.html', {'form': form})


def Login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        # print(form.is_valid())
        if form.is_valid():
            # use authenticate() to verify user's credentials
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('blogApp:Home_Page')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = UserLoginForm()
    return render(request, 'Users/Login.html', {'form': form})