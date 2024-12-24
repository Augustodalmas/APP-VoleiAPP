from django import forms
from Partida.models import Partida


class formPartida(forms.ModelForm):
    HORARIOS = [
        ('08:00', '08:00'),
        ('09:00', '09:00'),
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('12:00', '12:00'),
        ('13:00', '13:00'),
        ('14:00', '14:00'),
        ('15:00', '15:00'),
        ('16:00', '16:00'),
        ('17:00', '17:00'),
        ('18:00', '18:00'),
        ('19:00', '19:00'),
        ('20:00', '20:00'),
        ('21:00', '21:00'),
        ('22:00', '22:00'),
        ('23:00', '23:00'),
        ('00:00', '00:00'),
    ]

    hora = forms.ChoiceField(choices=HORARIOS, widget=forms.Select(
        attrs={'class': 'form-select'}))

    nivel = forms.ChoiceField(
        choices=Partida.NIVEL, widget=forms.Select(attrs={'class': 'form-select'}))

    rotacao = forms.ChoiceField(
        choices=Partida.ROTACAO, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Partida
        fields = ['titulo', 'descricao', 'nivel',
                  'rotacao', 'data', 'hora', 'local', 'lotacao']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'descricao': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descreva a partida...'}),
            'local': forms.TextInput(attrs={'placeholder': 'Exemplo: Quadra A, Arena X'}),
            'lotacao': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Número de vagas'}),
        }

    def clean_lotacao(self):
        lotacao = self.cleaned_data.get('lotacao')
        if lotacao <= 0:
            raise forms.ValidationError('A lotação deve ser maior que 0.')
        return lotacao
