from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import login

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not password1 or not password2:
            messages.error(request, 'Todos os campos são obrigatórios.')
        elif password1 != password2:
            messages.error(request, 'As senhas não coincidem.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Este nome de usuário já está em uso.')
        else:
            user = User.objects.create_user(username=username, password=password1)
            user.save()
            messages.success(request, 'Usuário criado com sucesso! Agora você pode fazer login.')
            login(request, user)
            return redirect(reverse_lazy('login'))

    return render(request, 'registration/registration.html')
