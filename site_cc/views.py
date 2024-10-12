from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Clube, Categoria, Avaliacao, Membro, Comentario
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q
from .models import Clube, Categoria, Modalidade, Comentario,Profile, Membro
import json
from django.contrib.auth.models import User

def pagina_principal(request):
    return render(request, 'pagina_principal.html')

def about(request):
    return render(request, 'about.html')

def introducao(request):
    return render(request, 'introducao.html')

def equipe(request):
    return render(request, 'equipe.html')

def contato(request):
    return render(request, 'contato.html')

@login_required

def clubes_view(request):
    nome = request.GET.get('nome', '')
    clubes = Clube.objects.all()
    categoria = request.GET.get('categoria')

    if nome:
        clubes = clubes.filter(Q(titulo__icontains=nome))
    
    if categoria and categoria != 'null': 
        clubes = clubes.filter(categoria__nome=categoria) 
     
    user = request.user
    clubes_context = [
        {
            'clube': clube,
            'user_is_member': Membro.objects.filter(clube=clube, usuario=user, aprovado=True).exists(),
            'user_request_pending': Membro.objects.filter(clube=clube, usuario=user, aprovado=False).exists(),
        }
        for clube in clubes.order_by('-dataDeCriacao')
    ]

    context = {
        'clubes_context': clubes_context,
        'cat_menu': Categoria.objects.all(),
    }
    return render(request, 'clubs.html', context)


@login_required
def meus_clubes_view(request):
    clubes = Clube.objects.filter(
        Q(moderador=request.user) | 
        Q(membros__usuario=request.user, membros__aprovado=True) |
        Q(privado=False, membros__usuario=request.user)
    ).distinct()

    nome_clube = request.GET.get('nome')
    if nome_clube:
        clubes = clubes.filter(titulo__icontains=nome_clube)

    context = {'object_list': clubes.order_by('-dataDeCriacao')}
    return render(request, 'myclubes.html', context)

@login_required
def add_categoria_view(request):
    if request.method == 'POST':
        nome_categoria = request.POST.get('nome')
        Categoria.objects.create(nome=nome_categoria)
        return redirect('addClube')

    return render(request, 'addCategoria.html')

@login_required
def add_club_view(request):
    return clube_create_view(request)

@login_required
def add_comentario_view(request, pk):
    return comentario_create_view(request, pk)

@login_required
def update_club_view(request, pk):
    return clube_update_view(request, pk)

@login_required
def clube_create_view(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        modalidade_id = request.POST.get('modalidade')
        categoria_id = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        sobre = request.POST.get('sobre')
        privado = request.POST.get('privado') == 'on'

        modalidade = Modalidade.objects.get(id=modalidade_id) if modalidade_id else None
        categoria = Categoria.objects.get(id=categoria_id) if categoria_id else None

        clube = Clube.objects.create(
            moderador=request.user,
            titulo=titulo,
            modalidade=modalidade,
            categoria=categoria,
            descricao=descricao,
            sobre=sobre,
            privado=privado
        )
        return redirect('club-Detail', pk=clube.pk)

    modalidades = Modalidade.objects.all()
    categorias = Categoria.objects.all()

    return render(request, 'addClube.html', {
        'modalidades': modalidades,
        'categorias': categorias,
    })

@login_required
def clube_update_view(request, pk):
    clube = get_object_or_404(Clube, pk=pk)

    if request.method == 'POST':
        clube.titulo = request.POST.get('titulo')
        modalidade_id = request.POST.get('modalidade')
        categoria_id = request.POST.get('categoria')
        clube.descricao = request.POST.get('descricao')
        clube.sobre = request.POST.get('sobre')
        clube.privado = request.POST.get('privado') == 'on'

        clube.modalidade = Modalidade.objects.get(id=modalidade_id) if modalidade_id else None
        clube.categoria = Categoria.objects.get(id=categoria_id) if categoria_id else None

        clube.save()
        return redirect('club-Detail', pk=clube.pk)

    modalidades = Modalidade.objects.all()
    categorias = Categoria.objects.all()

    return render(request, 'updateClube.html', {
        'clube': clube,
        'modalidades': modalidades,
        'categorias': categorias,
    })

@login_required
def comentario_create_view(request, clube_id):
    clube = Clube.objects.get(pk=clube_id)

    if request.method == 'POST':
        comentario_texto = request.POST.get('comentario')
        nome_usuario = request.user.username  
        Comentario.objects.create(
            clube=clube,
            nome=nome_usuario, 
            comentario=comentario_texto  
        )
        return redirect('club-Detail', pk=clube.pk)

    return render(request, 'addComentario.html', {'clube': clube})

def login_user(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            messages.success(request, "Você está logado.")
            return redirect('pagina_principal')
        messages.error(request, "Ocorreu um erro. Tente novamente.")
        return redirect('login')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "Você saiu.")
    return redirect('pagina_principal')

def CategoriaView(request, cats):
    categoria_clube = Clube.objects.filter(categoria__nome=cats.replace('-', ' '))
    return render(request, 'categorias.html', {'cats': cats.replace('-', ' '), 'categoria_clube': categoria_clube})

def home_page_view(request):
    clubes = Clube.objects.all().order_by('-dataDeCriacao')
    return render(request, 'pagina_principal.html', {'object_list': clubes})

def club_detail_view(request, pk):
    clube = get_object_or_404(Clube, id=pk)
    user = request.user
    progresso_percentual = (clube.progresso_atual / clube.total_capitulos * 100) if clube.total_capitulos > 0 else 0

    context = {
        'clube': clube,
        'total_avaliacoes': clube.total_avaliacoes(),
        'media_avaliacoes': clube.calcular_media_avaliacoes(),
        'progresso_percentual': round(progresso_percentual),
        'user_is_member': Membro.objects.filter(clube=clube, usuario=user, aprovado=True).exists(),
        'user_request_pending': Membro.objects.filter(clube=clube, usuario=user, aprovado=False).exists(),
    }
    return render(request, 'clubDetail.html', context)

def delete_club_view(request, pk):
    clube = get_object_or_404(Clube, pk=pk)
    if request.method == 'POST':
        clube.delete()
        return redirect('pagina_principal')

    context = {'clube': clube}
    return render(request, 'deleteClube.html', context)

def avaliacao_view(request, pk):
    if request.method == "POST":
        clube = get_object_or_404(Clube, id=pk)
        rating = int(request.POST.get('rating'))
        if 1 <= rating <= 5:
            Avaliacao.objects.update_or_create(
                clube=clube, usuario=request.user, defaults={'valor': rating}
            )
        return HttpResponseRedirect(reverse('club-Detail', args=[clube.id]))

def aprovar_membro(request, clube_id, membro_id):
    clube = get_object_or_404(Clube, id=clube_id)
    membro = get_object_or_404(Membro, id=membro_id, clube=clube)
    if request.user == clube.moderador:
        membro.aprovado = True
        membro.save()
    return JsonResponse({'status': 'success', 'message': 'Membro aprovado com sucesso!', 'membro_id': membro_id})

def recusar_membro(request, clube_id, membro_id):
    clube = get_object_or_404(Clube, id=clube_id)
    membro = get_object_or_404(Membro, id=membro_id, clube=clube)
    if request.method == 'POST':
        membro.delete()
    return JsonResponse({'status': 'success', 'message': 'Membro recusado com sucesso!', 'membro_id': membro_id})

def adicionar_membro(request, clube_id):
    clube = get_object_or_404(Clube, id=clube_id)
    Membro.objects.get_or_create(clube=clube, usuario=request.user, defaults={'aprovado': False})
    return redirect('clubs')

def adicionar_membro_publico(request, clube_id):
    clube = get_object_or_404(Clube, id=clube_id)
    if not clube.privado:
        Membro.objects.get_or_create(clube=clube, usuario=request.user, defaults={'aprovado': True})
    return redirect('clubs')



def atualizar_progresso(request, clube_id):
    if request.method == 'POST' and request.user.is_authenticated:
        clube = get_object_or_404(Clube, pk=clube_id)

        if request.user == clube.moderador:
            data = json.loads(request.body)  

            current_capitulo = int(data.get('current_capitulo', 0))
            total_capitulos = int(data.get('total_capitulos', 1)) 

            clube.progresso_atual = current_capitulo
            clube.total_capitulos = total_capitulos
            clube.save()

            progresso_percentual = (clube.progresso_atual / clube.total_capitulos * 100) if clube.total_capitulos > 0 else 0
            return JsonResponse({'success': True, 'redirect_url': clube.get_absolute_url(), 'progress_percent': progresso_percentual})

    return JsonResponse({'success': False})



@login_required
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)  
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        bio = request.POST.get('bio', '')  
        if bio:
            profile.bio = bio  
            profile.save() 
            return redirect('profile', user_id=user.id)  

    return render(request, 'profile.html', {'profile': profile})  
    

@login_required
def seguir_usuario(request, user_id):
    user = request.user
    usuario_a_seguir = get_object_or_404(User, id=user_id)
    
    profile, created = Profile.objects.get_or_create(user=user)

    if usuario_a_seguir not in profile.seguindo.all():
        profile.seguindo.add(usuario_a_seguir)
        profile.save()
    return redirect('profile', user_id=usuario_a_seguir.id)
def lista_usuarios(request):
    
    nome = request.GET.get('nome', '')

    
    if nome:
        usuarios = User.objects.filter(username__icontains=nome)
    else:
        usuarios = User.objects.all()

    return render(request, 'lista_usuarios.html', {'usuarios': usuarios, 'nome': nome})
  

