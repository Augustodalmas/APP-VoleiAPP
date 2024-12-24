from django.contrib import admin
from Partida.models import Partida, Participacao, HistoricoPartida


class PartidaAdministracao(admin.ModelAdmin):
    list_display = ('data', 'hora', 'local')


admin.site.register(Partida, PartidaAdministracao)
admin.site.register(Participacao)
admin.site.register(HistoricoPartida)
