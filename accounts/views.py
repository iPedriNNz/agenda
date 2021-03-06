from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    user = auth.authenticate(request, username=usuario, password=senha)
    if not user:
        messages.error(request, 'Login ou senha incorretos.')
        return redirect('index')
    else:
        auth.login(request, user)
        messages.success(request, 'Logado com sucesso.')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    messages.error(request, 'Deslogado com sucesso.')
    return redirect('index')


def register(request):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')
    if not nome or not sobrenome or not email or not usuario or not senha or not senha2:
        messages.error(request, 'Preencha todos os campos.')
        return redirect('register')
    try:
        validate_email(email)
    except:
        messages.error(request, 'E-mail inválido.')
        return redirect('register')
    if len(senha) < 6:
        messages.error(request, 'Sua senha deve ter no mínimo seis dígitos.')
        return redirect('register')
    if len(usuario) < 6:
        messages.error(request, 'Seu usuário deve ter no mínimo seis caracteres.')
        return redirect('register')
    if senha != senha2:
        messages.error(request, 'Suas senhas devem ser iguais.')
        return redirect('register')
    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Este usuário já está cadastrado.')
        return redirect('register')
    if User.objects.filter(email=email).exists():
        messages.error(request, 'Este e-mail já está cadastrado.')
        return redirect('register')
    messages.success(request, 'Registrado com sucesso! Faça seu login.')
    user = User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome, last_name=sobrenome)
    user.save()
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = FormContato(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Erro ao enviar formulário.')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})
    form.save()
    messages.error(request, 'Erro ao enviar formulário.')
    return redirect('dashboard')
