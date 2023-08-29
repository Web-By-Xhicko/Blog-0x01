from django import forms
from .models import Comment

class NewCommentForm(forms.ModelForm):
    Comment = forms.CharField(widget=forms.Textarea(attrs={'rows':10, 'cols':200 , 'class':'textarea','placeholder':'Comment'}))

    class Meta:
        model = Comment
        fields = ['Comment']




# class SearchForm(forms.Form):
#     Search_Input = forms.CharField()
