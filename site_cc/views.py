from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Clube, Categoria, Avaliacao, Membro, Comentario
from .forms import ClubeForm, ClubeEditForm, ComentarioForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q

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

class clubesView(LoginRequiredMixin, ListView):
    model = Clube
    template_name = 'clubs.html'
    ordering = ['-dataDeCriacao']

    def get_queryset(self):
        nome = self.request.GET.get('nome', '')
        clubes = Clube.objects.all()
        if nome:
            clubes = clubes.filter(Q(titulo__icontains=nome))
        return clubes.order_by('-dataDeCriacao')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = self.request.user
        clubes_context = [
            {
                'clube': clube,
                'user_is_member': Membro.objects.filter(clube=clube, usuario=user, aprovado=True).exists(),
                'user_request_pending': Membro.objects.filter(clube=clube, usuario=user, aprovado=False).exists(),
            }
            for clube in self.get_queryset()
        ]
        context.update({
            'clubes_context': clubes_context,
            'cat_menu': Categoria.objects.all(),
        })
        return context

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
        user = self.request.user
        context.update({
            'total_avaliacoes': clube.total_avaliacoes(),
            'media_avaliacoes': clube.calcular_media_avaliacoes(),
            'user_is_member': Membro.objects.filter(clube=clube, usuario=user, aprovado=True).exists(),
            'user_request_pending': Membro.objects.filter(clube=clube, usuario=user, aprovado=False).exists(),
        })
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

class AddComentarioView(CreateView):
    model = Comentario
    template_name = 'addComentario.html'
    form_class = ComentarioForm 

    def form_valid(self, form):
        comentario = form.save(commit=False)
        comentario.nome = self.request.user.username
        clube_id = self.kwargs.get('pk')
        if clube_id:
            comentario.clube = get_object_or_404(Clube, id=clube_id)
            comentario.save()
            return redirect('club-Detail', pk=comentario.clube.pk)
        form.add_error(None, 'Clube não encontrado.')
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clube_id'] = self.kwargs.get('pk')
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
            avaliacao, created = Avaliacao.objects.update_or_create(
                clube=clube, usuario=request.user, defaults={'valor': rating}
            )
        return HttpResponseRedirect(reverse('club-Detail', args=[clube.id]))

class meusclubesDetailView(ListView):
    model = Clube
    template_name = 'myclubes.html'
    ordering = ['-dataDeCriacao']

    def get_queryset(self):
        clubes = Clube.objects.filter(
            Q(moderador=self.request.user) | 
            Q(membros__usuario=self.request.user, membros__aprovado=True) |
            Q(privado=False, membros__usuario=self.request.user)
        )
        nome_clube = self.request.GET.get('nome')
        if nome_clube:
            clubes = clubes.filter(titulo__icontains=nome_clube)
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
    Membro.objects.get_or_create(clube=clube, usuario=request.user, defaults={'aprovado': False})
    return redirect('clubs')

def adicionar_membro_publico(request, clube_id):
    clube = get_object_or_404(Clube, id=clube_id)
    if not clube.privado:
        Membro.objects.get_or_create(clube=clube, usuario=request.user, defaults={'aprovado': True})
    return redirect('clubs')
