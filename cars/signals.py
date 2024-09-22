from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.db.models import Sum  # para fazer a soma no signal post_save
from django.dispatch import receiver
from cars.models import Car, CarInventory
# def criada para descrição das bios
from openai_api.client import get_car_ai_bio

# exemplos

# instance é objeto novo que será inserido no BD
# sender é o model que está enviado o evento. no caso é o model car
# **kwargs é para pegar tudo mais que for enviado
# o receicever é um decorator que ficará ouvindo tudo que acontece
# ai o receiver obriga o django a fazer a def abaixo ouvir tudo que está chegando em car, se for pre_save, entra na função

"""
@receiver(pre_save, sender=Car)  # executada antes de salvar
def car_pre_save(sender, instance, **kwargs):
    print('### PRE SAVE###')
    # claramente o sender é o cars model
    print('sender', sender)
    # claramente a instance mostra o objeto que está sendo cadastrado no BD
    print('instance', instance)

@receiver(pre_delete, sender=Car)  # executada antes de deletar
def car_pre_delete(sender, instance, **kwargs):
    print('### PRE DELETE ###')
    print('sender', sender)
    print('instance', instance)
"""
# como vamos usar apenas a parte do POST, comentei as PRE acima


# toda vez que não houver atualizão de codigo, tenho que mexer em todos os campos.
# logo, para uma boa prática, vamos criar uma def que faz o cars_count e cars_value
# e chamar ela no post_save e post_delete
def car_inventory_update():  # a explicação ta toda dentro da def car_post_save
    cars_count = Car.objects.all().count()
    cars_value = Car.objects.aggregate(
        total_value=Sum('value')
    )['total_value']
    CarInventory.objects.create(
        cars_count=cars_count,
        cars_value=cars_value
    )
# sempre que chegar um carro novo, atuliza o inventario


@receiver(post_save, sender=Car)  # executada depois de salvar
def car_post_save(sender, instance, **kwargs):
    # agora vamos usar apenas a funcção de atualizar o estoqye
    car_inventory_update()


"""  # para cada carro novo no estoque, vamos calcular 2 valor: cars_count e cars_value
    # cars_count com ORM
    # django pegue tudo que tem no BD de car e conte
    cars_count = Car.objects.all().count()

    # cars_values com ORM
    # pegue todos os valores que tem no BD e some
    cars_value = Car.objects.aggregate(  # aggregate cria um campo personalizado que retorna a agregação
        # o campo novo criado com a soma de todos os valores dos campos value
        total_value=Sum('value')
        # mas tudo isso vai me retorna um obj query, um dicionario com chave valor
        # {'total_value': 100.000}
        # mas só queremos ver o valor, o preço
    )['total_value']  # vai retornar apenas o valor
    # criando um registro no model CarInventory
    CarInventory.objects.create(
        cars_count=cars_count,  # aqui são os dados que serão passados
        cars_value=cars_value
    )"""


# sempre que houver uma deleção de carro, vamos atualizar o estoque


@receiver(post_delete, sender=Car)  # executada depois de deletar
def car_post_delete(sender, instance, **kwargs):
    car_inventory_update()


# agora vamos desenvolver um exemplo de pre-save
# se o usuario cadastrar um carro sem bio, essa def vai verificar isso. Se não tiver bio, vamos criar uma automatica
@receiver(pre_save, sender=Car)
def car_pre_save(sender, instance, **kwargs):
    if not instance.bio:  # se a instancia de carro não tem bio
        # to passando a def que importei e nos parametros dela to informando é para pegar
        # na instancia que o usuario ta passando o modelo, marca e ano do carro para
        # o chatgpt criar a bio sozinho
        instance.bio = 'Bora vender'

        # ai_bio = get_car_ai_bio(
        #     instance.model, instance.brand, instance.model_year
        # )
        # instance.bio = ai_bio  # aqui ta recebendo e salvando no campo bio
