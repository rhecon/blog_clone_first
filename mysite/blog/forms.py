from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):


    class Meta:
        model = Post
        fields = ('author','title', 'text',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
            # editable means we can edit it, medium-editor-textarea gives it the styling of the actual medium-editor, postcontent is our own class
        }


class CommentForm(forms.ModelForm):
        
        class Meta:
            model = Comment
            fields = ('author', 'text',)

            widgets = {
                'author': forms.TextInput(attrs={'class': 'textinputclass'}),
                'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
            }



# This is how to connect specific widgets (form content) to CSS styling