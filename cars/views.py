# from django.shortcuts import render, redirect
from cars.models import Car  # importando para expor no site
from cars.forms import CarModelForm
# para nos redirecionar para o car detail depois de editado
from django.urls import reverse_lazy
# usuario so pode entrar se tiver autenticado
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator  # para usar o decorator
# from django.views import View  # class da CBV
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView  # filha da View


"""def cars_view(request):  # as views só retornam HTML, CSS e JS.
    # select * from Car - mesma coisa que o codigo abaixo
    # retorna uma QuerySet - Aqui já é o ORM
    # cars = Car.objects.all()  # pegue todos obj que estão no cars
    # pegue todos obj que estão no cars aplicando este filtro
    # __ significa que to usando a FK e acessando a table brand
    # cars = Car.objects.filter(brand__name='Fiat')
    # select * from Car where model = 'Uno de firma'
    # __contains tudo com nome UNO (tem que ter a acentução correta da palavra)
    # posso usar tbm o icontains (para ignorar o CASE da fonte)
    # cars = Car.objects.filter(model__contains='Uno')
    # order_by ordena a apresentação pelo campo que você quiser, nesse caso model
    cars = Car.objects.all().order_by('model')

    search = request.GET.get('search')

    # captura todos os paramentros que queremos
    # print(request.GET.get('search'))
    # print(request.GET)  # QueryDict com as chave valor

    if search:  # se o user tiver feito uma busca
        # cars vai receber cars com filtro igual ao que user digitou no search
        # icontains -> ignora a caixa alta ou baixa
        # order_by ordena a apresentação pelo campo que você quiser, nesse caso model
        cars = cars.filter(model__icontains=search)

    # paramentros: request; caminho do arquivo HTML; context
    # como django sabe qual a pasta é (templates), só precisa do nome do arquivo
    # context é um dicionario de dados com a lista de todos os carros no BD
    return render(request,  # renderiza o html com a linguagem do django
                  'cars.html',  # dentro do template cars, rederize o context
                  {'cars': cars},  # dados de carros no BD
                  )
"""
# agora vamos escrever a a cars_view como CBV
# quando a requisção chegar em CarsView, vai ser executada a função dispatch() herdada de View


"""class CarsView(View):  # nossa CBV CarsView herda de View
    # função get pertence a view
    # o django verifica a requisão do usuário, se o metodo for get, executa a def abaixo
    def get(self, request):  # esse get() ta usando as mesmas coisas da def antiga que ta comentada
        # vantagem: organização, herança de view
        cars = Car.objects.all().order_by('model')
        search = request.GET.get('search')

        if search:
            cars = cars.filter(model__icontains=search)

        return render(request, 'cars.html', {'cars': cars})
        # essas def são endpoint de aprensentação."""

# reescrevendo a CarsView com a ListView
# para ser uma listview, tem que ser get. Logo, não preciso passar o metodo get como na class acima


class CarsListView(ListView):  # só com isso, a view já ta feita
    model = Car  # esse é o obj car que criamos em models.py
    template_name = 'cars.html'
    # objeto com os dados carregados do BD que vai p dentro do template
    context_object_name = 'cars'

    # filtro de pesquisa
    def get_queryset(self):  # minha query que é executada no BD
        # isso é personalizado para nossa busca, se fosse só o padrão, seria assim:
        # return Car.objects.all()
        # super() é uma def para acessar os metodos da ListView
        # nesse caso, o metodo é o get_queryset
        # o queryset é o Car que defini lá em cima
        cars = super().get_queryset().order_by('model')
        search = self.request.GET.get('search')

        if search:
            cars = cars.filter(model__icontains=search)
        return cars

# class para detalhe dos carros


class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'


"""def new_car_view(request):  # mesmo procedimento da def de cima
    # quando o usuario preencher os dados do carro (POST)
    if request.method == 'POST':
        # POST para os dados, FILES para as imagens
        new_car_form = CarModelForm(request.POST, request.FILES)

        if new_car_form.is_valid():  # se o cadastro for válido
            new_car_form.save()  # salve em new car (def criada em forms)
            return redirect('cars_list')  # redirecione para cars list

    else:
        new_car_form = CarModelForm()  # quando apenas eu entrar em new_car (GET)

    return render(request,
                  'new_car.html',  # se tiver dúvidas, voltar na aula 55
                  # variavel que está sendo exibida em new_car.html
                  {'new_car_form': new_car_form},
                  )"""
# agora vamos reescrever essa FBV new_car_view para CBV NewCarView


"""class NewCarView(View):  # sempre olhar os comentarios da def acima

    def get(self, request):  # quando for get, retorna form vazio
        new_car_form = CarModelForm
        return render(request, 'new_car.html', {'new_car_form': new_car_form})

    def post(self, request):  # faz a mesam coisa que a def anterior
        new_car_form = CarModelForm(request.POST, request.FILES)

        if new_car_form.is_valid():
            new_car_form.save()
            return redirect('cars_list')
        # se não for valido, vamos retorna um form com os erros
        return render(request, 'new_car.html', {'new_car_form': new_car_form})"""

# reescrevendo NewCarView com CreateView
# todos esses parametros estão dentro da CreateView, portanto consulte-a

# o decator vai executar o login_required que vai verificar se o usuario ta logado ou não. Caso não esteja, nem entra na view


@method_decorator(login_required(login_url='login'), name='dispatch')
class NewCarCreateView(CreateView):  # abaixo são os parametros necessários
    model = Car  # pegando do models.py
    form_class = CarModelForm  # determinando o form para criar
    template_name = 'new_car.html'
    success_url = '/cars/'  # url que o usuario vai depois que cadastrar um carro


@method_decorator(login_required(login_url='login'), name='dispatch')
class CarUpdateView(UpdateView):
    model = Car  # pega Car do models.py
    # por ser uma update view, vai ter o form de cadastro de carros
    form_class = CarModelForm
    template_name = 'car_update.html'
    # success_url = '/cars/'  # apos a edição, volta para cars
    # success_url = '/car/<int:pk>' # assim não funciona

    # subescrenvendo a success_url para ela nos direcionar para o carro editado
    def get_success_url(self):
        # me redirecione para car_detail onde o id vai ser com o nome pk e pegando a pk do objeto que estou no momento
        # ou seja, o id do carro que estou alterando
        return reverse_lazy('car_detail', kwargs={'pk': self.object.pk})


@method_decorator(login_required(login_url='login'), name='dispatch')
class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete.html'
    success_url = '/cars/'
