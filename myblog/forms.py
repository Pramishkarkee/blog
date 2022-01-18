from dataclasses import fields
from django.forms import ModelForm, models
from django.contrib.auth import get_user_model

from myblog.models import Blog,Comment, Like



class CreateWriter(ModelForm):
    class Meta:
        model = Blog
        fields = ['user','title','blog']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['user','blog','comment']

class LikeForm(ModelForm):
    class Meta:
        model = Like
        fields = ['user','blog']