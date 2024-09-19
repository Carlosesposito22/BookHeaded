from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def pagina_principal(request):
    return render(request,'pagina_principal.html',{})
def login_user(request):
    if request.method =="POST":
        username= request.POST['username']
        password= request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("voce esta logado"))
            return redirect('pagina_principal')


        else:   
            messages.success(request, ("ocorreu um erro tente novamente"))
            return redirect('login') 
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("voce deslogou"))
    return redirect('pagina_principal')

