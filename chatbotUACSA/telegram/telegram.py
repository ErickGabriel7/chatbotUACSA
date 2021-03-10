from flask import Flask, request
from requests import get

from chatbotUACSA.chat.processing import create_answer

app = Flask(__name__)

with open('bot_token', 'r') as file:
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


def send_picture(picture, body):
    if app.config['ENV'] == 'development':
        print('\n [ENVIANDO IMAGEM]:', picture, '\n')
    else:
        # adicionar código para enviar imagem
        pass