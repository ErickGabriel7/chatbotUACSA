from flask import Flask, request
from pro import processar_resposta
import requests

app = Flask(__name__)

BOT_TOKEN = "1418502829:AAHem_GKULQO7eDZtnKNcGRCbUR_x6Fv3Z8"  # Não disponibilizar para outras pessoas!


@app.route('/nova-mensagem', methods=["POST"])
def new_message():
    # pegando a mensagem com os dados que o telegram enviou
    body = request.json
    app.logger.info(f"Chegou uma nova mensagem: {body}")

    resposta = montar_resposta(body)
    enviar_mensagem(resposta, body)

    # falar para o telegram que tudo ocorreu bem
    return {'ok': True}


def montar_resposta(body):
    # verificando se a mensagem e um texto
    if 'text' in body['message']:
        texto_recebido = body['message']['text']
        nome_usuario = body['message']['from']['first_name']
        # quando um novo usuário inicia uma conversa com o bot, a primeira mensagem é sempre '\start'
        if texto_recebido == '/start':
            return f"Olá, {nome_usuario}!\nEu sou o chatbot de dúvidas da UACSA \U0001F601 \nEm que posso ajudar?"
        return processar_resposta(texto_recebido, nome_usuario)
    else:
        return f"Desculpe, só processo mensagens de texto por enquanto \U00002639 "


def enviar_mensagem(texto, body):
    endpoint = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": body['message']['chat']['id'],
        "text": texto,
    }
    requests.get(endpoint, params)
