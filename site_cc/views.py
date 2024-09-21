from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Clube, Categoria,Membro
from .forms import ClubeForm, ClubeEditForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


def pagina_principal(request):
    return render(request,'pagina_principal.html',{})

def about(request):
    return render(request, 'about.html')

class clubesView(LoginRequiredMixin, ListView):
    model = Clube
    template_name = 'clubs.html'
    ordering = ['-dataDeCriacao']

    def get_context_data(self, *args, **kwargs):
        context = super(clubesView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = Categoria.objects.all()
        return context
    
def login_user(request):
    if request.method =="POST":
        username= request.POST['username']
        password= request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You are logged in."))
            return redirect('pagina_principal')


        else:   
            messages.success(request, ("An error occured. Try again"))
            return redirect('login') 
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You logged out"))
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

class UpdateClubView(UpdateView):
    model = Clube
    template_name = 'updateClube.html'
    form_class = ClubeEditForm

class DeleteClubView(DeleteView):
    model = Clube
    template_name = 'deleteClube.html'
    success_url = reverse_lazy('pagina_principal')



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
def adicionar_membro_publico(request, clube_id):
    clube = get_object_or_404(Clube, id=clube_id)
    
    if clube.privado:
        
        return redirect('club-Detail', pk=clube.pk)

    
    Membro.objects.get_or_create(clube=clube, usuario=request.user, defaults={'aprovado': True})
    
    return redirect('club-Detail', pk=clube.pk)    