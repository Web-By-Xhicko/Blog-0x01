from django.shortcuts import redirect, render
from django.contrib.auth import authenticate , login
from .forms import UserRegistrationForm
from django.contrib import messages
from django.utils.safestring import mark_safe


def Register(request):
    if request.method == 'POST':
         form = UserRegistrationForm(request.POST)
         if form.is_valid():
             form.save()
             username = form.cleaned_data.get('username')
             messages.success(request, mark_safe( f'Account Sucessfully created for {username}! &nbsp; &nbsp; Welcome to Infohub!'))
             return redirect('blogApp:Home_Page')
    else:
        form = UserRegistrationForm()
    return render(request, 'Users/Register.html', {'form': form})


