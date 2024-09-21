from django import forms
from .models import Clube, Categoria, Modalidade


class ClubeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        self.fields['modalidade'].choices = [('', 'Selecione a modalidade')] + list(Modalidade.objects.all().values_list('id', 'nome'))
        self.fields['categoria'].choices = [('', 'Selecione a categoria')] + list(Categoria.objects.all().values_list('id', 'nome'))

    class Meta:
        model = Clube
        fields = ('moderador', 'titulo', 'modalidade', 'categoria', 'descricao', 'livroAtual', 'privado')
        widgets = {
            'moderador': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Selecione o moderador'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insira o título do clube'}),
            'modalidade': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descreva o clube'}),
            'livroAtual': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insira o livro atual'}),
            'privado': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }


class ClubeEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adicionar placeholders para as opções de seleção no formulário de edição também
        self.fields['modalidade'].choices = [('', 'Selecione a modalidade')] + list(Modalidade.objects.all().values_list('id', 'nome'))
        self.fields['categoria'].choices = [('', 'Selecione a categoria')] + list(Categoria.objects.all().values_list('id', 'nome'))

    class Meta:
        model = Clube
        fields = ('titulo', 'modalidade', 'categoria', 'descricao', 'livroAtual', 'privado')
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insira o título do clube'}),
            'modalidade': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descreva o clube'}),
            'livroAtual': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insira o livro atual'}),
            'privado': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
