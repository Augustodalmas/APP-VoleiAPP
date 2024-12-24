from django import forms
from User.models import perfilUsuario
from datetime import date


class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = perfilUsuario
        fields = [
            'username', 'email', 'data_nascimento', 'numero_telefone', 'cpf',
            'cidade', 'posicao', 'nivel', 'rotacao', 'pontuacao', 'foto',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'AAAA-MM-DD'}, format='%Y-%m-%d',),
            'numero_telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'cidade': forms.Select(attrs={'class': 'form-control'}),
            'posicao': forms.Select(attrs={'class': 'form-control'}),
            'nivel': forms.Select(attrs={'class': 'form-control'}),
            'rotacao': forms.Select(attrs={'class': 'form-control'}),
            'pontuacao': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
        }
