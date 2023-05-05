from django.urls import path
from .import views
# from  .views import PostListView

app_name = 'blogApp'

urlpatterns = [
    # path('Search/', views.Search_Item, name='Search_Page'),
    path('', views.PostListView, name='Home_Page'),
    path('<slug:S_post>/', views.Single_Post, name='Single_Post'),
    path('Category/<Category>/', views.CategoryListView.as_view(), name='Category')
] 