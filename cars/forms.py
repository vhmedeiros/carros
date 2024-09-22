from django import forms
from cars.models import Brand, Car  # importando a class brand p usar lá em baixo

# essa tabela serãos campos que o user vai preencher no site, então
# todos os campos que tem na class Car em models.py serão add aqui


# class CarForm(forms.Form):  # esse é mais lento e trabalhoso para criar.
#     model = forms.CharField(max_length=200)
#     # ModelChoiceFiled é mostrar para o cliente as lista de marcas que existem quando ele for preencher um novo carro
#     # estou buscando todas as Brands da minha table Brand
#     brand = forms.ModelChoiceField(Brand.objects.all())
#     factory_year = forms.IntegerField()
#     model_year = forms.IntegerField()
#     plate = forms.CharField(max_length=10)
#     value = forms.FloatField()
#     photo = forms.ImageField()

#     def save(self):  # o self indica que tudo acontecerá nesse mesmo objeto
#         # salvando o que o user digita lá no site
#         car = Car(
#             model=self.cleaned_data['model'],
#             brand=self.cleaned_data['brand'],
#             factory_year=self.cleaned_data['factory_year'],
#             model_year=self.cleaned_data['model_year'],
#             plate=self.cleaned_data['plate'],
#             value=self.cleaned_data['value'],
#             photo=self.cleaned_data['photo'],
#         )
#         car.save()  # esse save é diferente do de cima, esse é o que vai para o BD
#         return car

# esse Objeto é proprio para criar forms rapida e melhoradamente

# esse form (CarModelForm) que to criando vai ser em cima da class Car
# esse form de baixo subtitui tudo que escrevemos acima


class CarModelForm(forms.ModelForm):  # ele se liga com o obj Car

    class Meta:  # do model Car, eu quero esses campos abaixo
        model = Car  # pegando a tabela Car
        fields = '__all__'  # pegando todos os campos de Car

    # usando clean o django já entende que o campo apos o _ será usado para validação
    # portanto, sempre que tiver validação, já use o campo certo
    def clean_value(self):  # self é uma instancia do proprio form
        # captura para mim (self) o valor do campo value que o user mandou no form
        # cleaned_data é uma def nativa do form que retorna os dados limpos e validados que foram inseridos
        value = self.cleaned_data.get('value')

        if value < 20000:
            # na minha propria instancia (self) vou add um erro que pede 2 parametros: campo do erro; mensagem do erro
            self.add_error(
                'value', 'Valor minímo do carro deve ser de R$ 20.000,00')

        return value  # caso não caia no if, retorna valor inserido

    # carros antes de 1975 não serão vendidos na plataforma
    def clean_factory_year(self):
        factory_year = self.cleaned_data.get('factory_year')

        if factory_year < 1975:
            self.add_error(
                'factory_year', 'Ano mínimo do carro deve ser 1975.')

        return factory_year
