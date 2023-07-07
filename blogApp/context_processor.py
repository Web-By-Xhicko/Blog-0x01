from .models import Category, Comment

def Category_List_Options(request):
    Category_List_Options = Category.objects.exclude(name='Default')
    return {'Category_List_Options' : Category_List_Options}

def Comments(request, S_post):
   count = S_post.Comment.filter(Status=True)
   return {'comment_count': count}

# def User_Profile_Picture(request):
#     User_Profile_Picture = User_Profile.objects.all()
#     return {'User_Profile_Picture' : User_Profile_Picture}