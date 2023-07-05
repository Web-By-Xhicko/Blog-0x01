from django.urls import path
from .import views
# from  .views import PostListView

app_name = 'blogApp'

urlpatterns = [
    # path('Search/', views.Search_Item, name='Search_Page'),
    path('', views.PostListView, name='Home_Page'),
    path('Settings/', views.Settings, name='Settings_Page'),
    path('Profile/', views.Profile, name='Profile_Page'),
    path('Update_Profile/', views.Update_Profile, name='UpdateProfile_Page'),
    path('likes/', views.likes, name='likes'),
    path('<slug:S_post>/', views.Single_Post, name='Single_Post'),
    path('Category/<Category>/', views.CategoryListView.as_view(), name='Category'),
] 