from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Clube, Categoria, Avaliacao, Membro, Comentario
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q
from .models import Clube, Categoria, Modalidade, Comentario, Profile, Membro, HistoricoMaratona, Enquete, Opcao, Voto
import json
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.http import JsonResponse, HttpResponseBadRequest


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
    categorias = request.GET.getlist('categoria') 

    if nome:
        clubes = clubes.filter(Q(titulo__icontains=nome))
    
    if categorias: 
        clubes = clubes.filter(categoria__nome__in=categorias)  

    no_clubs_found = clubes.count() == 0  # Verifica se nenhum clube foi encontrado

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
        'no_clubs_found': no_clubs_found,  # Passa a informação de que nenhum clube foi encontrado
    }
    return render(request, 'clubs.html', context)





@login_required
def meus_clubes_view(request):
    clubes = Clube.objects.filter(
        Q(moderador=request.user) | 
        Q(membros__usuario=request.user, membros__aprovado=True) |
        Q(privado=False, membros__usuario=request.user)
    ).distinct()

    clubes_favoritos = request.user.clubes_favoritos.all()

    clubes_nao_favoritados = clubes.exclude(favoritos=request.user)

    nome_clube = request.GET.get('nome')
    if nome_clube:
        clubes_favoritos = clubes_favoritos.filter(titulo__icontains=nome_clube)
        clubes_nao_favoritados = clubes_nao_favoritados.filter(titulo__icontains=nome_clube)

    context = {
        'object_list': clubes_nao_favoritados.order_by('-dataDeCriacao'),
        'clubes_favoritos': clubes_favoritos.order_by('-dataDeCriacao'),
    }
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

    return render(request, 'clubDetail.html', {
        'clube': clube,
        'modalidades': modalidades,
        'categorias': categorias
    })

def get_modalidades(request):
    modalidades = Modalidade.objects.all().values('id', 'nome')
    return JsonResponse(list(modalidades), safe=False)

def get_categorias(request):
    categorias = Categoria.objects.all().values('id', 'nome')
    return JsonResponse(list(categorias), safe=False)

@login_required
def comentario_create_view(request, clube_id):
    clube = Clube.objects.get(pk=clube_id)

    if request.method == 'POST':
        comentario_texto = request.POST.get('comentario').strip()  # Remove espaços em branco

        # Verifica se o campo de comentário está vazio
        if not comentario_texto:
            messages.error(request, 'O comentário não pode estar vazio.')
            return render(request, 'addComentario.html', {'clube': clube})

        # Se o comentário não for vazio, prossegue para salvar
        Comentario.objects.create(
            clube=clube,
            user=request.user, 
            comentario=comentario_texto  
        )

        messages.success(request, 'Comentário adicionado com sucesso!')
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
    total_maratona_finalizadas = clube.total_maratona_finalizadas
    top_livros = clube.top_livros.split('\n') if clube.top_livros else []
    now = timezone.now()
    enquetes_ativas = clube.enquetes.filter(prazo__gte=now)
    enquetes_expiradas = clube.enquetes.filter(prazo__lt=now)

    context = {
        'clube': clube,
        'total_avaliacoes': clube.total_avaliacoes(),
        'media_avaliacoes': clube.calcular_media_avaliacoes(),
        'progresso_percentual': round(progresso_percentual),
        'user_is_member': Membro.objects.filter(clube=clube, usuario=user, aprovado=True).exists(),
        'user_request_pending': Membro.objects.filter(clube=clube, usuario=user, aprovado=False).exists(),
        'total_maratona_finalizadas': total_maratona_finalizadas,
        'top_livros': top_livros,
        'now': timezone.now(),
        'enquetes_ativas': enquetes_ativas,
        'enquetes_expiradas': enquetes_expiradas
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
    clube = get_object_or_404(Clube, id=pk)
    
    if request.method == "POST":
        rating = request.POST.get('rating')
        
        # Verificar se o valor de rating foi fornecido e é válido
        if rating and rating.isdigit() and 1 <= int(rating) <= 5:
            Avaliacao.objects.update_or_create(
                clube=clube, usuario=request.user, defaults={'valor': int(rating)}
            )
            return HttpResponseRedirect(reverse('club-Detail', args=[clube.id]))
        else:
            # Se o rating for inválido, retornar a página com uma mensagem de erro
            return render(request, 'clubDetail.html', {
                'clube': clube,
                'error_message': "Este campo é obrigatório e deve ser um número entre 1 e 5."
            })

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

    membro_existente = Membro.objects.filter(clube=clube, usuario=request.user).exists()

    if membro_existente:

        return HttpResponseBadRequest("Você já solicitou acesso a este clube.")

    Membro.objects.create(clube=clube, usuario=request.user, aprovado=False)
    
    url = reverse('myclubes')
    return redirect(f'{url}?modal=clubeModal-{clube_id}')

def adicionar_membro_publico(request, clube_id):
    clube = get_object_or_404(Clube, id=clube_id)
    if not clube.privado:
        Membro.objects.get_or_create(clube=clube, usuario=request.user, defaults={'aprovado': True})
    url = reverse('myclubes')
    return redirect(f'{url}?modal=clubeModal-{clube_id}')

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
    
    # Obtendo os clubes que o usuário favoritou
    clubes_favoritos = Clube.objects.filter(favoritos=user)  # Use 'user' em vez de 'request.user'
    
    seguidores = profile.seguidores.all()  
    seguindo = Profile.objects.filter(seguidores=user)  

    icons = [
        'images/icon1.svg',
        'images/icon2.svg',
        'images/icon3.svg',
        'images/icon4.svg',
        'images/icon5.svg',
        'images/icon6.svg',
        'images/icon7.svg',
        'images/icon8.svg',
        'images/icon9.svg',
        'images/icon10.svg',
        'images/icon11.svg',
        'images/icon12.svg',
        'images/icon13.svg',
        'images/icon14.svg',
        'images/icon15.svg',
    ]

    seguidores_count = profile.seguidores.count()  
    seguindo_count = seguindo.count()  

    if request.method == 'POST':
        bio = request.POST.get('bio', '')
        icone = request.POST.get('icone', '')

        if bio:
            profile.bio = bio

        if icone:  
            profile.icone = icone  

        profile.save()  
        return redirect('profile', user_id=user.id)  

    return render(request, 'profile.html', {
        'profile': profile,
        'seguidores': seguidores,
        'seguindo': seguindo,  
        'icons': icons,
        'seguidores_count': seguidores_count,
        'seguindo_count': seguindo_count,
        'clubes_favoritos': clubes_favoritos,  # Adicionando clubes favoritos ao contexto
    })




@login_required
def seguir_usuario(request, user_id):
    if request.method == 'POST':
        perfil = get_object_or_404(Profile, user__id=user_id)

        if request.user in perfil.seguidores.all():
           
            perfil.seguidores.remove(request.user)
        else:
            
            perfil.seguidores.add(request.user)
        
        perfil.save()

        return redirect('profile', user_id=user_id)
   
def lista_usuarios(request):
    nomes = request.GET.get('nomes', '')

    if nomes:
        usuarios = User.objects.filter(username__icontains=nomes)
    else:
        usuarios = User.objects.all()

    last_searches = request.session.get('last_searches', [])

    if nomes:
        if nomes not in last_searches:
            last_searches.insert(0, nomes)
        last_searches = last_searches[:5]
        request.session['last_searches'] = last_searches

    
    user_links = {user.username: user for user in User.objects.filter(username__in=last_searches)}

    return render(request, 'lista_usuarios.html', {
        'usuarios': usuarios,
        'nomes': nomes,
        'last_searches': last_searches,
        'user_links': user_links,
    })


@login_required
def favoritar_clube(request, clube_id):
    clube = get_object_or_404(Clube, id=clube_id)

    if request.user in clube.favoritos.all():
        clube.favoritos.remove(request.user)
        favoritado = False
    else:
        clube.favoritos.add(request.user)
        favoritado = True

    return JsonResponse({'favoritado': favoritado})



@login_required
def add_top_livros(request, clube_id):
    clube = get_object_or_404(Clube, id=clube_id)

    if request.user != clube.moderador:
        return JsonResponse({'error': 'Você não tem permissão para modificar os livros deste clube'}, status=403)

    if request.method == 'POST':
        top_livros = request.POST.get('top_livros', '').strip()
        clube.top_livros = top_livros
        clube.save()
        return redirect('club-Detail', pk=clube_id)
    
    return JsonResponse({'error': 'Método inválido'}, status=400)

from django.http import JsonResponse
import json
from datetime import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def criar_maratona_view(request, clube_id):
    clube = get_object_or_404(Clube, pk=clube_id)

    if request.method == 'POST':
        data = json.loads(request.body)
        nome_maratona = data.get('nome_maratona')
        data_fim_str = data.get('data_fim')
        capitulo_final = data.get('capitulo_final')
        capitulo_atual = data.get('capitulo_atual')
        data_inicio_str = data.get('data_inicio')

        try:
            data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()
            data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()

            if data_fim < data_inicio:
                return JsonResponse({'success': False, 'message': 'Data final não pode ser menor que a data inicial.'}, status=400)

            if capitulo_final < capitulo_atual:
                return JsonResponse({'success': False, 'message': 'Capítulo final não pode ser menor que o capítulo atual.'}, status=400)

            if clube.maratona_ativa:
                clube.nome_maratona = nome_maratona  
                clube.data_inicio_maratona = data_inicio 
                clube.data_fim_maratona = data_fim
                clube.capitulo_final_maratona = capitulo_final
                clube.capitulo_atual_maratona = capitulo_atual
                clube.save()  
                return JsonResponse({'success': True, 'message': 'Maratona atualizada com sucesso!'})

            clube.maratona_ativa = True
            clube.data_inicio_maratona = data_inicio
            clube.data_fim_maratona = data_fim
            clube.capitulo_final_maratona = capitulo_final
            clube.capitulo_atual_maratona = capitulo_atual
            clube.nome_maratona = nome_maratona  
            clube.save()  

            return JsonResponse({'success': True, 'message': 'Maratona criada com sucesso!'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    if clube.maratona_ativa:
        return JsonResponse({
            'success': True,
            'nome_maratona': clube.nome_maratona,
            'data_fim': clube.data_fim_maratona.strftime('%Y-%m-%d'),
            'data_inicio': clube.data_inicio_maratona.strftime('%Y-%m-%d'),
            'capitulo_final': clube.capitulo_final_maratona,
            'capitulo_atual': clube.capitulo_atual_maratona,
        })
    else:
        return JsonResponse({'success': False, 'message': 'Nenhuma maratona ativa'}, status=404)



@receiver(post_save, sender=Clube)
def verificar_maratona(sender, instance, **kwargs):
    if instance.maratona_ativa and instance.data_fim_maratona and instance.data_fim_maratona < timezone.now().date():
        
        instance.progresso_atual = instance.capitulo_final_maratona
        instance.maratona_ativa = False
        instance.save()
@login_required
def detalhes_maratona_view(request, clube_id):
    clube = get_object_or_404(Clube, pk=clube_id)
    
    if clube.maratona_ativa:
        return JsonResponse({
            'success': True,
            'maratona_ativa': True,
            'nome_maratona': clube.nome_maratona,
            'data_fim': clube.data_fim_maratona.strftime('%Y-%m-%d'),
            'data_inicio': clube.data_inicio_maratona.strftime('%Y-%m-%d'),
            'capitulo_final': clube.capitulo_final_maratona,
            'capitulo_atual': clube.capitulo_atual_maratona,
        })
    else:
        return JsonResponse({'success': True, 'maratona_ativa': False})

@login_required
def finalizar_maratona_view(request, clube_id):
    clube = get_object_or_404(Clube, pk=clube_id)
    
    if request.method == 'POST' and clube.maratona_ativa:
        try:
            HistoricoMaratona.objects.create(
                clube=clube,
                nome_maratona=clube.nome_maratona,
                data_fim=clube.data_fim_maratona,
                data_inicio=clube.data_inicio_maratona,
                capitulo_final=clube.capitulo_final_maratona,
                capitulo_atual=clube.capitulo_atual_maratona,
            )

            clube.progresso_atual = clube.capitulo_final_maratona
            clube.maratona_ativa = False
            clube.total_maratona_finalizadas += 1  
            clube.save()

            return JsonResponse({'success': True, 'message': 'Maratona finalizada com sucesso!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Método inválido'}, status=400)

@login_required
def listar_historico_maratona_view(request, clube_id):
    clube = get_object_or_404(Clube, pk=clube_id)
    historico = HistoricoMaratona.objects.filter(clube=clube).order_by('-data_registro')

    historico_data = [
        {
            'nome_maratona': h.nome_maratona,
            'data_fim': h.data_fim.strftime('%Y-%m-%d'),
            'data_inicio': h.data_inicio.strftime('%Y-%m-%d'),
            'capitulo_final': h.capitulo_final,
            'capitulo_atual': h.capitulo_atual,
            'data_registro': h.data_registro.strftime('%Y-%m-%d %H:%M:%S')
        }
        for h in historico
    ]

    return JsonResponse({'success': True, 'historico': historico_data})

@login_required
def sair_do_clube(request, clube_id):
    clube = get_object_or_404(Clube, id=clube_id)
    membro = Membro.objects.filter(clube=clube, usuario=request.user).first()

    if membro:
        membro.delete()

        if request.user in clube.favoritos.all():
            clube.favoritos.remove(request.user)

        messages.success(request, f'Você saiu do clube "{clube.titulo}"')
    else:
        messages.error(request, 'Você não faz parte deste clube.')

    return redirect('myclubes')
from django.views.decorators.csrf import csrf_exempt


def deletar_historico(request, username):
    if request.method == 'POST':
        user_searches = request.session.get('last_searches', [])
        if username in user_searches:
            user_searches.remove(username)
            request.session['last_searches'] = user_searches
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def criar_enquete_view(request, clube_id):
    clube = get_object_or_404(Clube, id=clube_id)

    if request.user != clube.moderador:
        messages.error(request, "Apenas moderadores podem criar enquetes.")
        return redirect('club-Detail', pk=clube.id)
    
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        prazo = request.POST.get('prazo')

        if not titulo or not prazo:
            messages.error(request, "Título e prazo são obrigatórios.")
            return redirect('club-Detail', pk=clube.id)

        try:
            prazo = timezone.datetime.strptime(prazo, '%Y-%m-%d').date()
            hoje = timezone.localdate()

            if prazo < hoje:
                messages.error(request, "A data de encerramento não pode ser no passado.")
                return redirect('club-Detail', pk=clube.id)
            
            enquete = Enquete.objects.create(clube=clube, moderador=request.user, titulo=titulo, prazo=prazo)

            opcoes_texto = request.POST.getlist('opcoes')
            for texto in opcoes_texto:
                if texto.strip():
                    Opcao.objects.create(enquete=enquete, texto=texto.strip())

            messages.success(request, "Enquete criada com sucesso!")
            return redirect('club-Detail', pk=clube.id)

        except ValueError:
            messages.error(request, "Data de prazo inválida.")
            return redirect('club-Detail', pk=clube.id)

    return render(request, 'criar_enquete.html', {'clube': clube})

@login_required
def votar_enquete(request, enquete_id):
    if request.method == "POST":
        usuario = request.user
        enquete = get_object_or_404(Enquete, id=enquete_id)

        try:
            data = json.loads(request.body)
            opcao_id = data.get('opcao_id')
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Dados inválidos no corpo da requisição.'})

        if not opcao_id:
            return JsonResponse({'success': False, 'message': 'Nenhuma opção foi selecionada.'})

        nova_opcao = get_object_or_404(Opcao, id=opcao_id, enquete=enquete)

        voto_existente = Voto.objects.filter(usuario=usuario, enquete=enquete).first()

        if voto_existente:
            voto_existente.opcao.votos.remove(usuario)
            voto_existente.opcao.save()

            voto_existente.opcao = nova_opcao
            voto_existente.save()
        else:
            Voto.objects.create(usuario=usuario, enquete=enquete, opcao=nova_opcao)

        nova_opcao.votos.add(usuario)
        nova_opcao.save()

        return JsonResponse({'success': True, 'message': 'Voto registrado com sucesso!'})

    return JsonResponse({'success': False, 'message': 'Requisição inválida.'})


def resultados_enquetes_view(request, clube_id):
    clube = get_object_or_404(Clube, id=clube_id)
    enquetes_data = []

    for enquete in clube.enquetes.all():
        opcoes_data = [
            {"texto": opcao.texto, "votos": opcao.votos.count()}
            for opcao in enquete.opcoes.all()
        ]
        enquetes_data.append({
            "id": enquete.id,
            "titulo": enquete.titulo,
            "prazo": enquete.prazo.strftime('%d/%m/%Y'),
            "opcoes": opcoes_data
        })

    return JsonResponse({"success": True, "enquetes": enquetes_data})