from django import forms
from .models import Post_Blog


class Post_Blog_Form(forms.ModelForm):
    class Meta:
        model =  Post_Blog
        fields = ('title','content','image','author','categories','tags','slug')