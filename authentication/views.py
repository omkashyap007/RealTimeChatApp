from django.shortcuts import render, redirect
from authentication.forms import LoginForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def getErrorList(errors):
    l = []
    for i in errors:
        for j in errors[i]:
            l.append(j)
    return l


def RegisterPage(request):
    if request.user.is_authenticated : 
        return redirect("chat-home")
    else : 
        if request.method == "POST":
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                user = authenticate(username = request.POST.get("username") , password = request.POST.get("password1"))
                login(request , user)
                return redirect("chat-home")
            else:
                errors = getErrorList(form.errors)
        else:
            errors = None
            form = UserRegisterForm()
        context = {"form": form , "errors" : errors}
        return render(request, "authentication/register.html", context)

def LoginPage(request):
    if request.user.is_authenticated : 
        return redirect("chat-home")
    else:
        errors = None
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect("chat-home")
            else :  
                errors = getErrorList(form.errors)
        else:
            form = LoginForm()
        context = {"form": form , "errors" : errors }
        return render(request, "authentication/login.html", context)


def LogoutPage(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("chat-home")
