from django import forms
from .models import Post


class CreatePost(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, required=True)
    image = forms.FileField(required=False)

    class Meta:
        model = Post
        fields = ['content', 'image']
