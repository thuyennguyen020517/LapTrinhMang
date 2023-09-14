from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
# Create your views here.


def index(request):
    return render(request, 'login_signup.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'my_register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_customer:
                login(request, user)
                return redirect('shopping')
            elif user is not None and user.is_superuser is True:
                login(request, user)
                return redirect('store')
            else:
                msg = 'error validating form'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})


def admin(request):
    return render(request,'admin.html')


def customer(request):
    return render(request,'customer.html')

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    response = redirect('login_view')
    response.delete_cookie('sessionid')
    return response
