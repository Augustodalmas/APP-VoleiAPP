from django.contrib import admin
from User.models import perfilUsuario, Cidade


class perfilUsuarioAdministracao(admin.ModelAdmin):
    list_display = ('username', 'data_nascimento',
                    'numero_telefone', 'cpf', 'cidade', 'posicao', 'nivel')


class cidadesAdministracao(admin.ModelAdmin):
    list_display = ('nome', 'estado')


admin.site.register(perfilUsuario, perfilUsuarioAdministracao)
admin.site.register(Cidade, cidadesAdministracao)
