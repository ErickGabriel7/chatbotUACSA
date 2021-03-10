from flask import Flask, request
from requests import get
import git

from chatbotUACSA.chat.processing import create_answer

app = Flask(__name__)

with open('chatbotUACSA/chatbotUACSA/telegram/bot_token', 'r') as file:
    BOT_TOKEN = file.readline()


@app.route('/nova-mensagem', methods=["POST"])
def receive_message():
    # pegando a mensagem com os dados que o telegram enviou
    body = request.json
    app.logger.info(f"Chegou uma nova mensagem: {body}")

    resposta = process_message(body)
    send_text_message(resposta, body)

    # falar para o telegram que tudo ocorreu bem
    return {'ok': True}


@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo()
        origin = repo.remotes.origin
        origin.pull()
        app.logger.info('Updated PythonAnywhere successfully')
        return 'Updated PythonAnywhere successfully', 200
    else:
        app.logger.info('Wrong event type')
        return 'Wrong event type', 400


def process_message(body):
    # verificando se a mensagem é um texto
    if 'text' in body['message']:
        texto_recebido = body['message']['text']
        nome_usuario = body['message']['from']['first_name']
        # quando um novo usuário inicia uma conversa com o bot, a primeira mensagem é sempre '\start'
        if texto_recebido == '/start':
            return f"Olá, {nome_usuario}!\nEu sou o chatbot não oficial de dúvidas da UACSA \U0001F601 \nEm que posso ajudar?"
        return create_answer(texto_recebido, nome_usuario)
    else:
        return f"Desculpe, só processo mensagens de texto por enquanto \U00002639 "


def send_text_message(text, body):
    if app.config['ENV'] == 'development':
        print('\n', text, '\n')
    else:
        endpoint = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        params = {
            "chat_id": body['message']['chat']['id'],
            "text": text,
        }
        get(endpoint, params)


def send_photo(photo_adress, body):
    if app.config['ENV'] == 'development':
        print('\n [ENVIANDO IMAGEM]:', photo_adress, '\n')
    else:
        # a imagem precisa estar no servidor, não funciona para url
        with open(photo_adress, 'rb') as photo:
            endpoint = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            params = {
                "chat_id": body['message']['chat']['id']
            }
            get(endpoint, params, files={'photo': photo})


def send_document(document_adress, body):
    if app.config['ENV'] == 'development':
        print('\n [ENVIANDO IMAGEM]:', document_adress, '\n')
    else:
        with open(document_adress, 'rb') as document:
            endpoint = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
            params = {
                "chat_id": body['message']['chat']['id']
            }
            get(endpoint, params, files={'document': document})
