from django.apps import AppConfig


class CarsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cars'

    # função para usarmos o signals
    def ready(self):  # ready diz que a aplicação está inicializando
        import cars.signals  # quando a aplicação for inicializada, importe o signals
