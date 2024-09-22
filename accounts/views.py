# UserCreationForm esse é o form para o register criar novos usuarios
# AuthenticationForm é para o login autenticar a entrada do user na aplicação
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# authenticate é o metodo que verifica se o username e password estão cadastrados no BD
# login é o metodo que executa o login
# logout faz o logout
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# criando a def para register
# precisamos identificar qual form o usuario vai usar para cadastrar


def register_view(request):
    if request.method == 'POST':
        # se o user tiver digitado os dados, criamos um novo usuario com esses dados
        user_form = UserCreationForm(request.POST)

        if user_form.is_valid():  # se for valido, cadastra novo usuario
            user_form.save()  # cadastra no bd
            return redirect('login')  # redireciona para a aba de login
        else:
            # user_form = UserCreationForm()  # caso contratio, vamos criar um form vazio
            # tive que colocar renderizando para receber os erros caso o user cadastre informações erradas
            return render(request, 'register.html', {'user_form': user_form})

    user_form = UserCreationForm()  # usando o form para cadastro de usuario
    return render(request, 'register.html', {'user_form': user_form})


def login_view(request):  # recebe a request e retorna um form ao user
    if request.method == 'POST':
        # verificando se digitou mesmo user e senha
        username = request.POST['username']
        password = request.POST['password']
        # verificando. recebe a requisição do usuario com os dados do login
        # e com o metodo auth... verifica no BD se tem isso cadastrado
        user = authenticate(request, username=username, password=password)

        if user is not None:  # se o user não for nulo, quer dizer que ele existe no BD
            # se o user é valido, faça login com a requisição passada pelo usuario
            login(request, user)  # o django já traz a função login pronta
            return redirect('cars_list')  # não coloque /, apenas o name da url

        else:
            login_form = AuthenticationForm()  # se tiver errado, retorna um form vazio

    else:
        login_form = AuthenticationForm()

    return render(request, 'login.html', {'login_form': login_form})


def logout_view(request):
    logout(request)  # usando o metodo logou que foi importado lá em cima
    return redirect('cars_list')
