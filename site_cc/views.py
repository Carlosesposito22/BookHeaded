from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Clube, Categoria, Avaliacao, Membro
from .forms import ClubeForm, ClubeEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect



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
        context["cat_menu"] = Categoria.objects.all()
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
        context['total_avaliacoes'] = self.object.avaliacao_set.count()  # Total de avaliações
        context['media_avaliacoes'] = self.object.calcular_media_avaliacoes()  # Média de avaliações
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clube = self.object
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

        
        clubes = clubes_moderados | clubes_membros
        return Clube.objects.filter(moderador=self.request.user).order_by('-dataDeCriacao')
        
    
def adicionar_membro(request, clube_id):
    clube = get_object_or_404(Clube, id=clube_id)
    if not Membro.objects.filter(clube=clube, usuario=request.user).exists():
        Membro.objects.create(clube=clube, usuario=request.user, aprovado=False)
    return redirect('club-Detail', pk=clube.pk)

def aprovar_membro(request, clube_id, membro_id):
    clube = get_object_or_404(Clube, id=clube_id)
    membro = get_object_or_404(Membro, id=membro_id, clube=clube)
    
    
    if request.user == clube.moderador:
        membro.aprovado = True
        membro.save()

    return redirect('club-Detail', pk=clube.pk)

def recusar_membro(request, clube_id, membro_id):
    clube = get_object_or_404(Clube, id=clube_id)
    membro = get_object_or_404(Membro, id=membro_id, clube=clube)
    
    if request.method == 'POST':
        membro.delete()  
        return redirect('club-Detail', pk=clube.pk)
