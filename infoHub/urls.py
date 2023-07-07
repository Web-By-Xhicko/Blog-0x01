from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from Users import views as UserLoginView
from Users import views as User_Views
from blogApp import views as User_Views2
from django.contrib.auth import views as auth_views
from Users.forms import PwdResetConfirmForm, PwdChangeForm

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', include('blogApp.urls', namespace='blogApp')),
    path('Register/', User_Views.Register, name='Register_Page'),
    path('Login/', User_Views.Login, name='Login_Page'),
    path('Logout/', User_Views.Logout, name='Logout_Page'),
    path('Password_Reset/', User_Views.PasswordResetFormPage.as_view(), name='Password_Reset_Page'),
    path('Password_Reset_Done/', User_Views.PassowrdResetDonePage.as_view(), name='password_reset_done'),
    path('Password_Reset_Confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='Users/password_reset_confirm.html', form_class=PwdResetConfirmForm), name='password_reset_confirm'),
    path('Password_Reset_Complete/', auth_views.PasswordResetCompleteView.as_view(template_name='Users/password_reset_complete.html'), name='password_reset_complete'),
    path('Change_Password/', auth_views.PasswordChangeView.as_view(template_name='Users/password_change.html', form_class=PwdChangeForm), name='Password_Change_Page'),
    path('Password_Done', auth_views.PasswordChangeDoneView.as_view(template_name='Users/password_change_done.html'), name='password_change_done'),
    path('delete/', User_Views2.Delete, name='Delete_Page' ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
