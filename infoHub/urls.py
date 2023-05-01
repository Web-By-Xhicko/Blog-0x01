from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from Users import views as UserLoginView
from Users import views as User_Views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Register/', User_Views.Register, name='Register_Page'),
    path('', include('blogApp.urls', namespace='blogApp')),
    # path('Login/', UserLoginView.UserLogin, name='UserLogin'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
