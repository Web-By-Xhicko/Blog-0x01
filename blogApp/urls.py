from django.urls import path
from .import views

app_name = 'blogApp'

urlpatterns = [
    # path('Search/', views.Search_Item, name='Search_Page'),
    path('', views.Home, name='Home_Page'),
    path('<slug:S_post>/', views.Single_Post, name='Single_Post'),
    path('Category/<Category>/', views.CategoryListView.as_view(), name='Category')
] 