from django import forms
from .models import Clube

class ClubeForm(forms.ModelForm):
    class Meta:
        model = Clube
        fields = ('moderador','titulo','modalidade','categoria','descricao','livroAtual','privado')
        widgets = {
            'moderador': forms.Select(attrs={'class':'form-control'}),
            'titulo': forms.TextInput(attrs={'class':'form-control'}),
            'modalidade': forms.Select(attrs={'class':'form-control'}),
            'categoria': forms.Select(attrs={'class':'form-control'}),
            'descricao': forms.Textarea(attrs={'class':'form-control'}),
            'livroAtual': forms.TextInput(attrs={'class':'form-control'}),
            'privado': forms.CheckboxInput(attrs={'class':'form-control'}),
        }

class ClubeEditForm(forms.ModelForm):
    class Meta:
        model = Clube
        fields = ('titulo','modalidade','categoria','descricao','livroAtual','privado')
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control'}),
            'modalidade': forms.Select(attrs={'class':'form-control'}),
            'categoria': forms.Select(attrs={'class':'form-control'}),
            'descricao': forms.Textarea(attrs={'class':'form-control'}),
            'livroAtual': forms.TextInput(attrs={'class':'form-control'}),
            'privado': forms.CheckboxInput(attrs={'class':'form-control'}),
        }