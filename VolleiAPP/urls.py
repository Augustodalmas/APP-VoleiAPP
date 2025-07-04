from django.contrib import admin
from django.urls import path, include
from User.views import profile, profileEdit
from django.conf.urls.static import static
from django.conf import settings
from User.views import main_page


urlpatterns = [
    path('', main_page, name='pagina_inicial'),
    path('admin/', admin.site.urls),
    path('partidas/', include('Partida.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', profile, name='account_profile'),
    path('accounts/profile/edit/', profileEdit.as_view(),
         name='account_profile_edit'),
    path('user/', include('User.urls')),
    # path('pagamento/', include('Pagamento.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# path('api/v1/', include('Times.urls')),
# path('api/v1/', include('Notificacao.urls')),
