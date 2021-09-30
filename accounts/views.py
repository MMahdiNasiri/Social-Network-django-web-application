from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateUserForm, LoginForm


# Create your views here.

def register_view(request):
    if request.method == 'POST':
        register_form = CreateUserForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            errkey = list(register_form.errors.as_data().keys())[0]
            if errkey == 'username':
                messages.error(request, 'نام کاربری موجود است ')
            if errkey == 'password1' or errkey == 'password2':
                messages.error(request, 'رمز عبور را تصحیح کنید')
    else:
        register_form = CreateUserForm()
    context = {'form': register_form}
    return render(request, 'accounts/register.html', context)


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است')

    return render(request, 'accounts/login.html', {'form': form})


@login_required(login_url='/accounts/login/')
def logout_view(request):
    logout(request)
    return redirect('login')

