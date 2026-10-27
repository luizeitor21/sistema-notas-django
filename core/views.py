from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Nota


def cadastrar(request):
    if request.method == 'POST':
        usuario_digitado = request.POST.get('username')
        senha_digitada = request.POST.get('password')
        senha2_digitada = request.POST.get('password2')

        
        if senha_digitada != senha2_digitada:
            return render(request, 'cadastrar.html', {'erro': 'As senhas não coincidem.'})

        if User.objects.filter(username=usuario_digitado).exists():
            return render(request, 'cadastrar.html', {'erro': 'Este nome de usuário já está em uso.'})

        
        User.objects.create_user(username=usuario_digitado, password=senha_digitada)
        return redirect('login')

    return render(request, 'cadastrar.html')


def pagina_login(request):
    if request.method == 'POST':
        usuario_digitado = request.POST.get('username')
        senha_digitada = request.POST.get('password')
        
        user = authenticate(request, username=usuario_digitado, password=senha_digitada)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'erro': 'Usuário ou senha incorretos.'})
            
    return render(request, 'login.html')


def sair(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/')
def dashboard(request):
    if request.method == 'POST':
        v_titulo = request.POST.get('titulo')
        v_conteudo = request.POST.get('conteudo')
        
        Nota.objects.create(usuario=request.user, titulo=v_titulo, conteudo=v_conteudo)
        return redirect('dashboard')
        
    minhas_notas = Nota.objects.filter(usuario=request.user)
    return render(request, 'dashboard.html', {'notas': minhas_notas})


@login_required(login_url='/')
def editar_nota(request, id):
    nota = get_object_or_404(Nota, id=id, usuario=request.user)

    if request.method == 'POST':
        nota.titulo = request.POST.get('titulo')
        nota.conteudo = request.POST.get('conteudo')
        nota.save()
        return redirect('dashboard')

    return render(request, 'editar_nota.html', {'nota': nota})


@login_required(login_url='/')
def deletar_nota(request, id):
    nota = get_object_or_404(Nota, id=id, usuario=request.user)
    nota.delete()
    return redirect('dashboard')
