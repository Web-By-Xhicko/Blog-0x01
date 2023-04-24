from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Post , Category
from .forms import NewCommentForm  # SearchForm#
from django.views.generic import ListView


class PostListView(ListView):
    model = Post
    template_name = 'blogApp/Index.html'
    context_object_name = 'Blog_Post'

        #returning all the informaton from the database into the queryset
    def get_queryset(self):
        Updated_Post = Post.Newmanager.order_by('-Publish')[:4]
        Older_Post = Post.Newmanager.order_by('Publish')[:8]
        return {'Updated_Post' : Updated_Post, 'Older_Post' : Older_Post }
    
        #Passing the information from the context variable to the html template
    def get(self, request, *args, **kwargs):
        context = self.get_queryset()
        return render(request, self.template_name, context)
    

    #Creates a single page of each post through s
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
        return render(request, 
               'blogApp/Single_Post.html', 
               {
                'S_post': S_post,
                'user_comment' : user_comment, 
                'Comment' : Comment,
                 'comment_form': comment_form,
                 'O_post' : O_post 
                  })


class CategoryListView(ListView):
    template_name = 'blogApp/Category_Pages.html'
    #passes the information about the category query from the database to the  html template 
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