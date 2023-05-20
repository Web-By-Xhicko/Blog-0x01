
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Post , Category
from .forms import NewCommentForm  # SearchForm#
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from Users.forms import UserProfileUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.shortcuts import redirect


@login_required
def Settings(request):
    return render(request, 'blogApp/settings.html' )

@login_required
def Profile(request):
    return render(request, 'blogApp/Profile.html' )

@login_required
def Update_Profile(request):
    if request.method == 'POST':
        UserProfileUpdate = UserProfileUpdateForm(request.POST, instance=request.user)
        ProfileUpdate = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if UserProfileUpdate.is_valid() and ProfileUpdate.is_valid():
            UserProfileUpdate.save()
            ProfileUpdate.save()
        messages.success(request, f'Your Profile has been updated successfully!')
        return redirect('blogApp:UpdateProfile_Page')

    else:
        UserProfileUpdate = UserProfileUpdateForm(instance=request.user)
        ProfileUpdate = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'UserProfileUpdate' : UserProfileUpdate,
        'ProfileUpdate' : ProfileUpdate
    }

    return render(request, 'blogApp/Update_Profile.html', context)


@login_required
def PostListView(request):
    updated_posts = Post.Newmanager.order_by('-Publish')[:4]
    older_posts = Post.Newmanager.order_by('Publish')[:8]
    context = {'Updated_Post': updated_posts, 'Older_Post': older_posts}
    return render(request, 'blogApp/Index.html', context)


@login_required
def Single_Post(request, S_post):
    S_post =  get_object_or_404(Post, slug=S_post, Status='published')
    Comment = S_post.Comment.filter(Status=True)
    user_comment = None
    O_post = Post.Newmanager.filter(Status='published').exclude(id=S_post.id)[:5]

    if request.method == 'POST':
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid(): 
            user_comment = comment_form.save(commit=False)
            user_comment.Post = S_post
            user_comment.save()
            return HttpResponseRedirect('/' + S_post.slug)
    else:
        comment_form = NewCommentForm()
        print(O_post)
        return render(request, 'blogApp/Single_Post.html', {'S_post': S_post,'user_comment' : user_comment, 
                'Comment' : Comment, 'comment_form': comment_form,'O_post' : O_post })

# @login_required
class CategoryListView(ListView):
    template_name = 'blogApp/Category_Pages.html'
    context_object_name = 'Category_List'

    def get_queryset(self):
       Category_Content = {
            #Captures a specific category Name  to the template
            'Category' : self.kwargs['Category'],
            #Collects all data from the post ||filters post from the specific category name  to specific category pages|| filters again to only published posts
            'Category_Post' : Post.Objects.filter(Category__name=self.kwargs['Category']).filter(Status='published')
        } 
       return Category_Content
    

# def Search_Item(request):
#     Form = SearchForm()
#     Query = ''
#     Search_Result = []

#     #checking to see if data exist in the Get request
#     if 'Query' in request.GET:
#         #Processing the information in request
#         Form = SearchForm(request.GET)
#         #checking to see if form is valid
#         if Form.is_valid():
#             #if form is valid, the data should be returned
#             Query = Form.cleaned_data['Query']
#             #Looking for the posts in the database that contains the query
#             Search_Result = Post.Objects.filter(Title__contains=Query)


#     return render(request, 'blogApp/Search.html', 
#                   {'Form':Form,
#                    'Query': Query,
#                    'Search_Result':Search_Result})