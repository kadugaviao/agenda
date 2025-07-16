from django.contrib import admin
from django.urls import path
from core import views
from django.views.generic import RedirectView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('eventos/<str:titulo_evento>', views.get_local_evento, name='get_local_evento'),
    path('agenda/', views.lista_eventos),
    path('', RedirectView.as_view(url='/agenda/')),
    path('login/', views.login_user),
    path('login/submit', views.submit_login),
    path('logout/', views.logout_user),
]
