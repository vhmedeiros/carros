"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# de dentro de cars no arquivo views importe cars_view
# from cars.views import CarsView, NewCarView  # agora estamos usando a CBV
# agora estamos usando a CBV ListView
from cars.views import CarsListView, NewCarCreateView, CarDetailView, CarUpdateView, CarDeleteView
from accounts.views import register_view, login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),  # caminho do site admin
    # 2 parametros: caminho do site, função do site que é uma view, name é para nomear essa url
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # normalmente se passa uma def para url; quando se usa CBV precisa do .as_view
    path('cars/', CarsListView.as_view(), name='cars_list'),
    # cada url tem uma view referente
    path('new_car/', NewCarCreateView.as_view(), name='new_car'),
    # car/id do carro. int primary key
    path('car/<int:pk>', CarDetailView.as_view(), name='car_detail'),
    # rota para editar os carros | ao entrar aqui, o user vai ser redirecionado para a CBV Update
    path('car/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
    # roda de deleção de carros | mesma coisa que a de cima, mas agora apaga o carro
    path('car/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# já está configurado o uso de imagens na aplicação
