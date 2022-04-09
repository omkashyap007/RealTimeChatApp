from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Enter the username !"}),
        required=True)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Enter the pasword !"}),
        required=True)

    class Meta:
        fields = ["username", "password"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user_count = User.objects.filter(username=username).count()
        if not user_count:
            raise forms.ValidationError(
                "The user with username \"{}\" does not exist .".format(username))
        return username

    def clean_password(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        try:
            user = User.objects.filter(username=username).first()
        except:
            user = None

        if user and not user.check_password(password):
            raise forms.ValidationError("Invalid Password !")

        return password


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=15, required=True , widget = forms.TextInput(
        attrs = {"placeholder" : "Create a username ..."}))
    email = forms.CharField(required=True , widget = forms.EmailInput(
        attrs = {"placeholder" : "Write your email address  ..."}))

    class Meta:
        model = User
        fields = ["username",  "email", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise forms.ValidationError("The username is required !")

        if len(str(username)) > 15:
            raise forms.ValidationError(
                "The length of the username should not exceed 15 letters !")

        count = User.objects.filter(username=username).count()

        if count:
            raise forms.ValidationError(
                "The username \"{}\" already exists !".format(username))

        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("")

        count = User.objects.filter(email=email).count()

        if count:
            raise forms.ValidationError("The email already exists !")

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if not password1:
            raise forms.ValidationError("The Password Field is required !")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "The two password fields do not match !")

        return password1


"""
omkashyap008
dfchndasfofacui904wr3247

"""
