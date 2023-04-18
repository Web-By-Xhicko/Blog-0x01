from .models import Category

def Category_List_Options(request):
    Category_List_Options = Category.objects.exclude(name='Default')
    return {'Category_List_Options' : Category_List_Options}


# def User_Profile_Picture(request):
#     User_Profile_Picture = User_Profile.objects.all()
#     return {'User_Profile_Picture' : User_Profile_Picture}