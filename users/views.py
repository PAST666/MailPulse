from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'Неверные учетные данные')
    return render(request, 'users/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                # Логиним и редиректим 
                login(request, user)
                return redirect('main')
            else:
                error = 'Пользователь с таким именем уже существует'
        else:
            error = 'Пароли не совпадают'
        
        # Негативный случай. Мы показываем ошибку пользователю
        return render(request, 'users/register.html', {'error': error})
    
    # Метод GET
    return render(request, 'users/register.html')

def logout_view(request):
    logout(request)
    return redirect('main')
