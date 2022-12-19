from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import redirect

def set_login_session_cookies(request, username, password):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        request.session['username'] = username
        request.session['password'] = password
        return request
    return request

def get_login_session_cookies(request):
    session = request.session
    if 'username' in session and 'password' in session:
        username = session.get('username', None)
        password = session.get('password', None)
        print('session data get')
        return username, password
    print('no session data')
    return None

def login_using_session(request):
    if get_login_session_cookies(request) != None:
        username , password = get_login_session_cookies(request)

        user = authenticate(request=request, username=username, password=password)
        if user:
            login(request, user=user)
            messages.success(request, 'Login success using session data')
            return redirect('/')
    print('dont have session login')