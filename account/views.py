from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account import utails
from shop.utails import DISTRICT_CHOICES, CITY_CHOICES
from shop.models import Customer

def account(request):
    request.session.set_test_cookie()
    return render(request, 'accounts/account.html')

@login_required
def profile(request):
    user = request.user

    default_cus = Customer.objects.filter(_user=user).first()
    all_cus = Customer.objects.filter(_user=user)
    context = {
        'districts': DISTRICT_CHOICES,
        'cities': CITY_CHOICES,
        'address': default_cus,
        'all_cus': all_cus,
    }
    return render(request, 'accounts/profile.html', context)

def login_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        user = authenticate(request, username=phone, password=password)
        if user:
            login(request, user=user)
            messages.success(request, 'Login success')
            
            if remember != None:
                utails.set_login_session_cookies(request, phone, password)

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
def change_password(request):
    user = request.user
    if request.method == 'POST':
        pre_pass = request.POST.get('pre-pass')
        new_pass = request.POST.get('new-pass')
        new_pass2 = request.POST.get('new-pass2')

        user = User.objects.get(pk=user.pk)
        if user and user.check_password(pre_pass):
            if new_pass == new_pass2:
                if len(new_pass) >= 6:
                    user.set_password(new_pass)
                    user.save()
                    messages.success(request, 'New Password set successfuly!')
                    return redirect('/account') # send to login page
                messages.error(request, 'New password must be atleast 6 charecters!')
                return redirect('/account/profile')
            messages.error(request, 'New password and confirm new password must be same')
            return redirect('/account/profile')
        messages.error(request, 'Wrong previous password!')
        return redirect('/account/profile')
    return redirect('/account/profile')


@login_required
def add_customer_address(request):
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        district = request.POST.get('district')
        city = request.POST.get('city')
        address = request.POST.get('address')

        # save address data to db
        cus = Customer.objects.create(_user=user, name=name, phone=phone, district=district, city=city, address=address)
        cus.save()
        messages.success(request, 'New address added successfuly!')
        return redirect('/account/profile')
    return redirect('/account/profile')

@login_required
def logout_view(request):
    request.session.clear_expired()
    
    logout(request)
    messages.success(request, 'Logout success')
    return redirect('/account')