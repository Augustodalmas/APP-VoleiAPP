from django import forms
from Partida.models import Partida, Local


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

    local = forms.ModelChoiceField(queryset=Local.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-select'}))

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

    def clean_lotacao(self):
        lotacao = self.cleaned_data.get('lotacao')
        if lotacao <= 0:
            raise forms.ValidationError('A lotação deve ser maior que 0.')
        return lotacao


class LocalForm(forms.ModelForm):
    class Meta:
        model = Local
        fields = ['nome', 'cidade', 'bairro', 'rua', 'numero', 'CEP']
        widgets = {
            'CEP': forms.TextInput(attrs={'placeholder': '00000-000'}),
        }

    def clean_CEP(self):
        cep = self.cleaned_data.get('CEP')
        if len(cep) != 9:
            raise forms.ValidationError(
                'CEP inválido. Certifique-se de usar o formato 00000-000.')
        return cep
