from django.contrib import admin
# na pasta cars no arquivo models importe Car e Brand
from cars.models import Car, Brand  # chamando Car e Brand para usar ele na def
# vai herdar do admin do obj modeladmin


class CarAdmin(admin.ModelAdmin):
    # estamos sobreescrevendo essas propriedades que vem do modeladmin
    # lista quais campos eu quero que apareçam na grade do dislpay
    list_display = ('model', 'brand', 'factory_year', 'model_year', 'value')
    # é o campo de busca que posso usar no site, digito o modelo do carro e ele busca
    search_fields = ('model', 'brand',)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_field = ('name',)


# essa def serve para indicar para o django criar e registrar a class CarAdmin no admin.py
# passamos 2 parametros: modelo que to usando, e as configuração do admin
admin.site.register(Car, CarAdmin)
admin.site.register(Brand, BrandAdmin)
