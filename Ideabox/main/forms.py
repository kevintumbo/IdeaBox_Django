from django import forms
from django.contrib.auth import (authenticate, get_user_model, login, logout, )
from .models import Idea, Comment
from pagedown.widgets import PagedownWidget


User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("The user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("The username or password is incorrect")
            return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "password2",
        ]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        username_qs = User.objects.filter(username=username)
        if username_qs.exists():
            raise forms.ValidationError("This Username is already being used")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This Email is already being used")
        return email

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Passwords not matching")
        return password


class IdeaForm(forms.ModelForm):
    title = forms.CharField()
    description = forms.CharField(widget=PagedownWidget)

    class Meta:
        model = Idea
        fields = [
            "title",
            "description",
        ]


class CommentForm(forms.ModelForm):
    comment = forms.Textarea()

    class Meta:
        model = Comment
        fields = [
            "comment",
        ]
