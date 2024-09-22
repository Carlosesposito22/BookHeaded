from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Clube, Categoria, Avaliacao, Membro, Comentario
from .forms import ClubeForm, ClubeEditForm, ComentarioForm  # Adicionado ComentarioForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse


def pagina_principal(request):
    return render(request, 'pagina_principal.html', {})

def about(request):
    return render(request, 'about.html')

class clubesView(LoginRequiredMixin, ListView):
    model = Clube
    template_name = 'clubs.html'
    ordering = ['-dataDeCriacao']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        clubes = context['object_list']
        cat_menu = Categoria.objects.all()

        clubes_context = []
        user = self.request.user

        for clube in clubes:
            user_is_member = Membro.objects.filter(clube=clube, usuario=user, aprovado=True).exists()
            user_request_pending = Membro.objects.filter(clube=clube, usuario=user, aprovado=False).exists()
            clubes_context.append({
                'clube': clube,
                'user_is_member': user_is_member,
                'user_request_pending': user_request_pending,
            })

        context['clubes_context'] = clubes_context
        context['cat_menu'] = cat_menu
        return context

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Você está logado.")
            return redirect('pagina_principal')
        else:
            messages.error(request, "Ocorreu um erro. Tente novamente.")
            return redirect('login')
    return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "Você saiu.")
    return redirect('pagina_principal')

def CategoriaView(request, cats):
    categoria_clube = Clube.objects.filter(categoria__nome=cats.replace('-', ' '))
    return render(request, 'categorias.html', {'cats': cats.replace('-', ' '), 'categoria_clube': categoria_clube})

class HomePageView(ListView):
    model = Clube
    template_name = 'pagina_principal.html'
    ordering = ['-dataDeCriacao']

class ClubDetailView(DetailView):
    model = Clube
    template_name = 'clubDetail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clube = self.object
        
        context['total_avaliacoes'] = clube.total_avaliacoes()
        context['media_avaliacoes'] = clube.calcular_media_avaliacoes()
        
        user = self.request.user
        context['user_is_member'] = Membro.objects.filter(clube=clube, usuario=user, aprovado=True).exists()
        context['user_request_pending'] = Membro.objects.filter(clube=clube, usuario=user, aprovado=False).exists()
        
        return context

class AddCategoriaView(CreateView):
    model = Categoria
    template_name = 'addCategoria.html'
    fields = '__all__'
    success_url = reverse_lazy('addClube')


class AddClubView(CreateView):
    model = Clube
    form_class = ClubeForm
    template_name = 'addClube.html'

    def form_valid(self, form):
        clube = form.save()
        return redirect('club-Detail', pk=clube.pk)


class AddComentarioView(CreateView):  # Classe para adicionar comentário
    model = Comentario
    template_name = 'addComentario.html'
    form_class = ComentarioForm  # Usando ComentarioForm

    def form_valid(self, form):
        comentario = form.save(commit=False)  # Não salva ainda no banco
        comentario.nome = self.request.user.username  # Preenche com o username do usuário

        # Verifica se 'clube_id' está presente na URL
        clube_id = self.kwargs.get('pk')  # Ajuste se a URL não usar 'clube_id'
        if clube_id:
            comentario.clube = get_object_or_404(Clube, id=clube_id)  # Associa ao clube
            comentario.save()  # Salva o comentário
            return redirect('club-Detail', pk=comentario.clube.pk)  # Redireciona para a página do clube
        else:
            # Lidar com o caso em que clube_id não está presente
            form.add_error(None, 'Clube não encontrado.')
            return self.form_invalid(form)  # Retorna o formulário inválido

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clube_id'] = self.kwargs.get('pk')  # Passa o clube_id para o contexto se precisar
        return context

class UpdateClubView(UpdateView):
    model = Clube
    template_name = 'updateClube.html'
    form_class = ClubeEditForm


class DeleteClubView(DeleteView):
    model = Clube
    template_name = 'deleteClube.html'
    success_url = reverse_lazy('pagina_principal')


def AvaliacaoView(request, pk):
    if request.method == "POST":
        clube = get_object_or_404(Clube, id=pk)
        rating = int(request.POST.get('rating'))

        if 1 <= rating <= 5:
            avaliacao_existente = Avaliacao.objects.filter(clube=clube, usuario=request.user).first()

            if avaliacao_existente:
                avaliacao_existente.valor = rating
                avaliacao_existente.save()
            else:
                Avaliacao.objects.create(clube=clube, usuario=request.user, valor=rating)
        return HttpResponseRedirect(reverse('club-Detail', args=[str(clube.id)]))


class meusclubesDetailView(ListView):
    model = Clube
    template_name = 'myclubes.html'
    ordering = ['-dataDeCriacao']

    def get_queryset(self):
        clubes_moderados = Clube.objects.filter(moderador=self.request.user)
        clubes_membros = Clube.objects.filter(membros__usuario=self.request.user, membros__aprovado=True)
        clubes_publicos = Clube.objects.filter(privado=False, membros__usuario=self.request.user)

        clubes = clubes_moderados | clubes_membros | clubes_publicos
        return clubes.distinct().order_by('-dataDeCriacao')


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
    if not Membro.objects.filter(clube=clube, usuario=request.user).exists():
        Membro.objects.create(clube=clube, usuario=request.user, aprovado=False)
    
    return redirect('clubs')


def adicionar_membro_publico(request, clube_id):
    clube = get_object_or_404(Clube, id=clube_id)
    if clube.privado:
        return redirect('clubs')
    Membro.objects.get_or_create(clube=clube, usuario=request.user, defaults={'aprovado': True})
    
    return redirect('clubs')

