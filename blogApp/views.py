from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Post , Category
from .forms import NewCommentForm  # SearchForm#
from django.views.generic import ListView

def Home(request):
    #populating all the post from the database to the html homepage 
    all_post = Post.Newmanager.all()
    #adding the post to the rendered html pages(homepage)
    return render(request, 'blogApp/Index.html', {'Posts' : all_post})

    #Creates a single page of each post through slug
def Single_Post(request, S_post):
    S_post =  get_object_or_404(Post, slug=S_post, Status='published')
    Comment = S_post.Comment.filter(Status=True)
    user_comment = None

#if the comment is eqaul to the post request on the template , the code should?
    if request.method == 'POST':
        #the post should know that the current request is a post request on the form templates
        comment_form = NewCommentForm(request.POST)
        #if the form is valid(coreect email and if they are no empty fields)
        if comment_form.is_valid():
            #the comment should be taken 
            user_comment = comment_form.save(commit=False)#takr the comment but dont save yet (commit=False)
            #populate the comment in the single page post
            user_comment.Post = S_post
            #save the comment on the single page sections for comments
            user_comment.save()
            #redirect the the page to the current page after it has been saved
            return HttpResponseRedirect('/' + S_post.slug)
    else:
        comment_form = NewCommentForm()
        return render(request, 
               'blogApp/Single_Post.html', 
               {
                #telling django waht it should display on the template
                #the single post of each post
                'S_post': S_post,
                #the user comments
                'user_comment' : user_comment, 
                #other comments
                'Comment' : Comment,
                #comment form
                 'comment_form': comment_form, 
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