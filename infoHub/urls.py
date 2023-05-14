from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from Users import views as UserLoginView
from Users import views as User_Views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Register/', User_Views.Register, name='Register_Page'),
    path('Login/', User_Views.Login, name='Login_Page'),
    path('Logout/', User_Views.Logout, name='Logout_Page'),
    path('Password_Reset/', User_Views.PasswordResetFormPage.as_view(), name='Password_Reset_Page'),
    path('Password_Reset_Done/', User_Views.PassowrdResetDonePage.as_view(), name='password_reset_done'),
    path('Password_Reset_Confirm/<uidb64>/<token>/', User_Views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('', include('blogApp.urls', namespace='blogApp')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
