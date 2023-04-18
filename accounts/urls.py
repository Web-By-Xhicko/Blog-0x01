from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import  PasswordResetForm,PasswordResetConfirmForm , UserLoginForm

app_name = 'accounts'

urlpatterns = [
  path('login/', auth_views.LoginView.as_view(template_name='registration/login.html',
                                              authentication_form=UserLoginForm), name='Login_Page'),
  path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html',
                                                       form_class=PasswordResetForm),name='PasswordReset_Page'), 
  path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html', form_class=PasswordResetConfirmForm),name='PasswordResetConfirm_Page'),
  path('profile/', views.account_profile, name='Profile_Page'), 
  # path('account_creation_message/', views.account_creation_message, name='account_creation_message'),
  path('register/', views.account_registration, name='Registration_Page'),
  # path('login/', views.login, name='Login_Page'),
  path('activate/<slug:uidb64>/<slug:token>', views.activate, name='Activate_Page'),
] 