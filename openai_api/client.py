"""from openai import OpenAI

client = OpenAI(
    api_key='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'
)


def get_car_ai_bio(model, brand, year):
    # o dicts se referem ao model, brand e ano que ta nos parametros da def
    # esse format é para substituir os dicts acima pelas variaveis abaixo.
    message = '''
    Me mostre uma descrição de venda para o carro {} {} {} em apenas 250 caracteres. 
    Fale coisas específicas do modelo.
    Descreve especificações técnicas do modelo do carro.'''

    message = message.format(brand, model, year)
    # essa é a responsta que a IA retorna
    response = client.chat.completions.create(
        messages=[
            {
                'role': 'user',
                'content': message,
            }
        ],
        max_tokens=50,  # sobre não estourar o limite de tokens
        model='gpt-3.5-turbo',  # modelo da IA tem na doc dela
    )
    # a resposta virá como obj json, então eu quero em choice o 1ª objeto de texto
    return response.choices[0].message.content
# _____________________________________________________________________________________________#
"""

"""import openai
import time
# Importe os erros diretamente da raiz
from openai import OpenAIError, RateLimitError

# Inicialize o cliente da OpenAI com a chave da API
# Substitua pela sua chave válida da OpenAI
openai.api_key = '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'


def get_car_ai_bio(model, brand, year):
    # Definindo o prompt para o modelo
    message = f'''
    Me mostre uma descrição de venda para o carro {brand} {model} {year} em apenas 250 caracteres.
    Fale coisas específicas do modelo. Descreva especificações técnicas do modelo do carro.
    '''

    # Tente criar uma resposta com retentativas em caso de erro de limite de taxa
    for attempt in range(3):  # Tenta 3 vezes
        try:
            response = openai.ChatCompletion.create(
                messages=[
                    {
                        'role': 'user',
                        'content': message,
                    }
                ],
                max_tokens=50,
                model='gpt-3.5-turbo',  # Use um modelo suportado
            )
            # Retorna a resposta gerada pelo modelo
            return response.choices[0].message.content
        except RateLimitError as e:
            print(f"Erro de limite de taxa: {e}. Retentando em 5 segundos...")
            time.sleep(5)  # Espera 5 segundos antes de tentar novamente
        except OpenAIError as e:  # Captura outros erros da API OpenAI
            print(f"Erro inesperado da OpenAI: {e}")
            break
        except Exception as e:
            print(f"Erro inesperado: {e}")
            break  # Para se houver outro erro que não seja da OpenAI

    return "Erro ao gerar a descrição do carro. Tente novamente mais tarde."
"""


import openai
import time
from openai import RateLimitError  # Certifique-se de que o erro está importado corretamente
client = openai.OpenAI(
    # Substitua pela sua chave válida da OpenAI
    api_key='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'
)


def get_car_ai_bio(model, brand, year):
    message = '''
    Me mostre uma descrição de venda para o carro {} {} {} em apenas 250 caracteres. Fale coisas específicas desse modelo.
    Descreva especificações técnicas desse modelo de carro.
    '''
    message = message.format(brand, model, year)

    for attempt in range(3):  # Tenta até 3 vezes em caso de erro de limite
        try:
            response = client.chat.completions.create(
                messages=[
                    {
                        'role': 'user',
                        'content': message
                    }
                ],
                max_tokens=1000,
                model='gpt-3.5-turbo',
            )
            return response.choices[0].message.content
        except RateLimitError as e:
            print(f"Erro de limite de taxa: {e}. Retentando em 5 segundos...")
            time.sleep(5)  # Espera 5 segundos antes de tentar novamente
        except Exception as e:
            print(f"Erro inesperado: {e}")
            break  # Se ocorrer um erro diferente, para a execução

    return "Erro ao gerar a descrição do carro. Tente novamente mais tarde."
