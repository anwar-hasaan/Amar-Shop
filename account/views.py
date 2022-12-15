from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def account(request):
    if request.method == 'POST':
        pass

    context = {
    }
    return render(request, 'accounts/account.html', context)

def login_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        user = authenticate(request, username=phone, password=password)
        if user:
            login(request, user=user)
            messages.success(request, 'Login success')
            
            next_page = request.GET.get('next')
            if next_page != 'None':
                return redirect(next_page)
            else:
                return redirect('/cart')
        messages.error(request, 'incorrect phone or password')
        return redirect('/account')

def register_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        user = User.objects.filter(username=phone).first()
        if user is not None:
            messages.error(request, f'User with \"{user.username}\" phone number already exists, try another')
            return redirect('/account')
        elif password != password2:
            messages.error(request, 'password and confirm password must be same')
            return redirect('/account')
        elif len(password) < 6:
            messages.error(request, 'password must contain at least 6 charecters')
            # return reverse('account:home')
            return redirect('/account')
        else:
            user = User.objects.create_user(username=phone, email=email)
            user.set_password(password)
            user.save()
            messages.error(request, 'registration successful')              
    return redirect('/account')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout success')
    return redirect('/account')