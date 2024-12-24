from django.shortcuts import render
from django.http import JsonResponse
import requests
from User.models import Cidade
from User.forms import EditarPerfilForm
from User.models import perfilUsuario
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


def carregar_cidades(request):
    if request.method == 'GET':
        url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
        response = requests.get(url)
        if response.status_code == 200:
            municipios = response.json()
            for municipio in municipios:
                Cidade.objects.get_or_create(
                    nome=municipio['nome'],
                    estado=municipio['microrregiao']['mesorregiao']['UF']['nome']
                )
            return JsonResponse({"message": "Cidades carregadas com sucesso!"})
        else:
            return JsonResponse({"error": "Erro ao carregar as cidades"}, status=500)


def profile(request):
    return render(request, 'account/profile.html')


def main_page(request):
    return render(request, 'main.html')


def ranking(request):
    usuarios = perfilUsuario.objects.all().order_by('-pontuacao')
    usuarios_limitados = usuarios[:10]
    return render(request, 'ranking.html', {'usuarios': usuarios_limitados})


class profileEdit(LoginRequiredMixin, UpdateView):
    model = perfilUsuario
    form_class = EditarPerfilForm
    template_name = 'account/profile_edit_infos.html'
    success_url = reverse_lazy('account_profile')

    def get_object(self):
        return self.request.user

    def get_initial(self):
        initial = super().get_initial()
        initial['data_nascimento'] = self.request.user.data_nascimento
        return initial
