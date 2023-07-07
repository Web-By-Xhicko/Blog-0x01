from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from Users.models import Profile
from .models import Post, Comment
from .forms import NewCommentForm  # SearchForm#
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from Users.forms import UserProfileUpdateForm, ProfileUpdateForm, PwdChangeForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import  JsonResponse
from django.db.models import Count


@login_required
def likes(request):
   if request.POST.get('action') == 'post':
       result = ''
       post_id = int(request.POST.get('postid'))
       post = get_object_or_404(Post, id=post_id)
       
       if post.likes.filter(id=request.user.id).exists():
           post.likes.remove(request.user)
           post.likes_count -= 1
           result = post.likes_count
           post.liked = False
           post.save()
       else:
           post.likes.add(request.user)
           post.likes_count  += 1
           result = post.likes_count
           post.liked = True
           post.save()


       return JsonResponse({'result':result, 'liked':post.liked,})
   

@login_required
def Delete(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        user.is_active = False
        user.save()
        messages.success(request,'Account Successfully Deleted!' )
        return redirect('Login_Page') 
    
    return render(request, 'Users/delete.html')

@login_required
def Settings(request):
    return render(request, 'blogApp/settings.html' )

@login_required
def Profile(request):
    return render(request, 'blogApp/Profile.html' )

@login_required
def Update_Profile(request):
    if request.method == 'POST':
        UserProfileUpdate = UserProfileUpdateForm(request.POST, instance=request.user, request = request)
        ProfileUpdate = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if UserProfileUpdate.is_valid() and ProfileUpdate.is_valid():
            UserProfileUpdate.save()
            ProfileUpdate.save()
            messages.success(request, f'Your Profile has been updated successfully!')
            return redirect('blogApp:UpdateProfile_Page')
    
    else:
        UserProfileUpdate = UserProfileUpdateForm(instance=request.user, request = request)
        ProfileUpdate = ProfileUpdateForm(instance=request.user.profile)
    
    FileName = request.user.profile.file_name
    context = {
        'UserProfileUpdate' : UserProfileUpdate,
        'ProfileUpdate' : ProfileUpdate,
        'FileName': FileName
    }

    return render(request, 'blogApp/Update_Profile.html', context)

@login_required
def PostListView(request):
    updated_posts = Post.Newmanager.annotate(num_comments=Count('Comment')).order_by('-Publish')[:4]
    older_posts = None
   
    if len(updated_posts) > 4:
         older_posts = Post.Newmanager.annotate(num_comments=Count('Comment')).order_by('Publish')[:8]

    context = {'Updated_Post': updated_posts,
               'Older_Post': older_posts,
            }
    
    return render(request, 'blogApp/index.html', context)

@login_required
def Single_Post(request, S_post):
    S_post =  get_object_or_404(Post, slug=S_post, Status='published')
    Comment = S_post.Comment.filter(Status=True)
    user_comment = None
    O_post = Post.Newmanager.annotate(num_comments=Count('Comment')).filter(Status='published')  #.exclude(id=S_post.id)[:5]
    if request.method == 'POST':
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid(): 
            user_comment = comment_form.save(commit=False)
            user_comment.Post = S_post
            user_comment.save()
            return HttpResponseRedirect('/' + S_post.slug)
    else:
        comment_form = NewCommentForm()
        return render(request, 'blogApp/Single_Post.html', {'S_post': S_post,'user_comment' : user_comment, 
                'Comment' : Comment, 'comment_form': comment_form,'O_post' : O_post, })


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