from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from Users import views as UserLoginView
from Users import views as User_Views
from Users import views 
from django.contrib.auth import views as Auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Register/', User_Views.Register, name='Register_Page'),
    path('Login/', User_Views.Login, name='Login_Page'),
    path('Logout/', User_Views.Logout, name='Logout_Page'),
    path('Password_Reset/', views.PasswordResetFormPage.as_view(), name='Password_Reset_Page'),
    path('', include('blogApp.urls', namespace='blogApp')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
