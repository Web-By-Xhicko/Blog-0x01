from django import forms
from .models import Comment

class NewCommentForm(forms.ModelForm):
    Name = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Tell Us your Name'}))
    Email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'input', 'placeholder':'Tell us Your Email'}))
    Comment = forms.CharField(widget=forms.Textarea(attrs={'rows':10, 'cols':200 , 'class':'textarea', 'placeholder':'Tell Us what You think about this post!'}))

    class Meta:
        model = Comment
        fields = ['Name', 'Email', 'Comment']


# class SearchForm(forms.Form):
#     Search_Input = forms.CharField()
