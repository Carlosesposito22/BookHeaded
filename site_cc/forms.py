from django import forms
from .models import Clube, Categoria, Modalidade, Comentario


class ClubeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['modalidade'].choices = [('', 'Selecione a modalidade')] + list(Modalidade.objects.all().values_list('id', 'nome'))
        self.fields['categoria'].choices = [('', 'Selecione a categoria')] + list(Categoria.objects.all().values_list('id', 'nome'))
        if 'class' in self.fields['privado'].widget.attrs:
            self.fields['privado'].widget.attrs['class'] = self.fields['privado'].widget.attrs['class'].replace('form-control', '').strip()

    class Meta:
        model = Clube
        fields = ('moderador', 'titulo', 'modalidade', 'categoria', 'descricao', 'sobre', 'privado')
        widgets = {
            'moderador': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'moderador', 'type': 'hidden'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insira o título do clube'}),
            'modalidade': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descreva em poucas palavras seu clube'}),
            'sobre': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Conte mais sobre o clube'}),
            'privado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),  # Ajuste a classe para checkbox
        }


class ClubeEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['modalidade'].choices = [('', 'Selecione a modalidade')] + list(Modalidade.objects.all().values_list('id', 'nome'))
        self.fields['categoria'].choices = [('', 'Selecione a categoria')] + list(Categoria.objects.all().values_list('id', 'nome'))

    class Meta:
        model = Clube
        fields = ('titulo', 'modalidade', 'categoria', 'descricao', 'sobre', 'privado')
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insira o título do clube'}),
            'modalidade': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descreva em poucas palavras seu clube'}),
            'sobre': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Conte mais sobre o clube'}),
            'privado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),  # Ajuste a classe para checkbox
        }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ('comentario',)
        widgets = {
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escreva seu comentário'}),
        }
