from dataclasses import fields
from django.forms import ModelForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CreateWriter(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']


class CreateAdminUser(ModelForm):
    class Meta:
        model = User
        fields = ['user_type', 'first_name', 'last_name', 'email', 'password']
