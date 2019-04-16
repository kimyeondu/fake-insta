from django import forms
from .models import Post, Image, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content',]
        widgets = {
            'content': forms.Textarea(
                attrs={'placeholder': 'Enter Content here'}),
        }
        
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['file',]
        widgets = {
            'file': forms.FileInput(attrs={'multiple': True}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]
        widgets = {
            'content': forms.Textarea(
                attrs={'placeholder': 'Enter Content here',
                    'rows':1,
                }),
        }