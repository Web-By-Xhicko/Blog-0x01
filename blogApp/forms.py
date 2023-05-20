from django import forms
from .models import Comment

class NewCommentForm(forms.ModelForm):
    Name = forms.CharField(widget=forms.TextInput(attrs={'class':'input'
                                                         , 'placeholder':'Username'}))
    Email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'input',
                                                             'placeholder':'Email'}))
    Comment = forms.CharField(widget=forms.Textarea(attrs={'rows':10, 'cols':200 ,
                                                            'class':'textarea',
                                                              'placeholder':'Comment'}))

    class Meta:
        model = Comment
        fields = ['Name', 'Email', 'Comment']




# class SearchForm(forms.Form):
#     Search_Input = forms.CharField()
