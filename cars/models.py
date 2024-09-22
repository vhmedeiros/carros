from django.db import models
# boa pratica, code em english

# o nome da class é a tabela no BD
# ela herda atributos da class Model

# tabela nova brand


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name  # pois quero que retorne o nome da marca


class Car(models.Model):
    # autofield é uma def que preenche automaticamente o id, autoincrementa
    id = models.AutoField(primary_key=True)  # primeiro campo da tabela Car
    # campo model vai ser uma str de tamanho max 200 caracters
    model = models.CharField(max_length=200)
    # brand é uma FK que vem da class Brand;
    # on_delete=PROTECT significa que a não pode deletar tal marca se tiver carros cadastrados
    # related_name é apenas o nome da relação de Car com Bran
    brand = models.ForeignKey(
        Brand, on_delete=models.PROTECT, related_name='car_brand')
    # ano de fabricacao é um campo inteiro
    factory_year = models.IntegerField(blank=True, null=True)
    model_year = models.IntegerField(blank=True, null=True)
    plate = models.CharField(max_length=10, blank=True,
                             null=True)  # placa do carro
    # preço é float - blank e null dizer que o campo não é obrigatorio ao cadastrar um novo carro
    value = models.FloatField(blank=True, null=True)
    # armazenar a referencia da imagem. toda foto deve ser armazenada na pasta cars/
    photo = models.ImageField(upload_to='cars/', blank=True, null=True)
    # campo para a descrição do carro, o textfield aceita textos gigantes
    bio = models.TextField(blank=True, null=True)

    # essa é uma def padrão que retorna o nome da propriedade que voce escoolhe
    # antes tava retornando carobjetc(1), agora vai retornar marea

    def __str__(self):
        return self.model


# invatario dos carros


class CarInventory(models.Model):
    cars_count = models.IntegerField()  # contage de estoque
    cars_value = models.FloatField()  # valor do estoque
    # ele vai se auto preencher no momento da criação
    created_at = models.DateTimeField(
        auto_now_add=True)  # data e hora de quando o registro foi criado

    # ordem decrescente de apresentação na aplicação
    class Meta:  # subescrevendo a class Meta
        # vai ordendar de forma decrescente a partir da data de criação.
        #  o "-" é justamente para pegar do mais recente
        ordering = ['-created_at']

    # formatação para apresentação do estoque
    def __str__(self):
        # pegando a instancia da quantidade de carro e a instancia do valor do estoque
        return f'{self.cars_count}' - {self.cars_value}
