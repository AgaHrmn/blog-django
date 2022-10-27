from django import forms
from .models import BlogPost, Comment

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('title', 'text', 'image')
        #labels = {'text': ''}    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('title', 'text',)
        labels = {'text': ''}

class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text' : ''}