from flask import Flask, request
from requests import get
from chatbotUACSA.chat.data_loading import script_dir
import git
import os

from chatbotUACSA.chat.processing import create_answer

app = Flask(__name__)

if app.config['ENV'] == 'development':
    with open('chatbotUACSA/telegram/bot_token', 'r') as file:
        BOT_TOKEN = file.readline()
else:
    with open('chatbotUACSA/chatbotUACSA/telegram/bot_token', 'r') as file:
        BOT_TOKEN = file.readline()


@app.route('/nova-mensagem', methods=["POST"])
def receive_message():
    # pegando a mensagem com os dados que o telegram enviou
    body = request.json
    app.logger.info(f"Chegou uma nova mensagem: {body}")

    resposta = process_message(body)
    send_answer(resposta, body)

    # falar para o telegram que tudo ocorreu bem
    return {'ok': True}


@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('chatbotUACSA/')
        origin = repo.remotes.origin
        origin.pull()
        app.logger.info('Updated PythonAnywhere successfully')
        return 'Updated PythonAnywhere successfully', 200
    else:
        app.logger.info('Wrong event type')
        return 'Wrong event type', 400


def send_answer(resposta, body):
    # Função que processa a resposta gerada e escolhe que tipo de função de envio usar.
    global there_is_img
    global there_is_text
    global there_is_doc
    try:
        if resposta['text'] is not None:
            there_is_text = True
    except KeyError:
        there_is_text = False
    try:
        if resposta['images'] is not None:
            there_is_img = True
    except KeyError:
        there_is_img = False
    try:
        if resposta['docs'] is not None:
            there_is_doc = True
    except KeyError:
        there_is_doc = False
    if there_is_text:
        if there_is_img:
            if there_is_doc:
                resposta_imagem = resposta['images']
                resposta_texto = resposta['text']
                resposta_documento = resposta['docs']
                app.logger.info(f"Resposta (send_photo e send_document): {resposta}")
                send_photo(resposta_imagem, body, caption=resposta_texto)
                send_document(resposta_documento, body)

            else:
                resposta_imagem = resposta['images']
                resposta_texto = resposta['text']
                app.logger.info(f"Resposta (send_photo): {resposta}")
                send_photo(resposta_imagem, body, caption=resposta_texto)
        else:
            if there_is_doc:
                resposta_documento = resposta['docs']
                resposta_texto = resposta['text']
                app.logger.info(f"Resposta (send_document): {resposta}")
                send_document(resposta_documento, body, caption=resposta_texto)
            else:
                resposta = resposta['text']
                app.logger.info(f"Resposta (send_text_message): {resposta}")
                send_text_message(resposta, body)
    elif there_is_doc:
        resposta_documento = resposta['docs']
        app.logger.info(f"Resposta (send_document): {resposta}")
        send_document(resposta_documento, body)
    else:
        if there_is_img:
            if there_is_doc:
                resposta_documento = resposta['docs']
                resposta_imagem = resposta['images']
                app.logger.info(f"Resposta (send_photo e send_document): {resposta}")
                send_photo(resposta_imagem, body)
                send_document(resposta_documento, body)
            else:
                resposta_imagem = resposta['images']
                app.logger.info(f"Resposta (send_photo): {resposta}")
                send_photo(resposta_imagem, body)

    pass


def process_message(body):
    # verificando se a mensagem é um texto
    if 'text' in body['message']:
        texto_recebido = body['message']['text']
        nome_usuario = body['message']['from']['first_name']
        # quando um novo usuário inicia uma conversa com o bot, a primeira mensagem é sempre '\start'
        if texto_recebido == '/start':
            return {'text': f'Olá, {nome_usuario}!\nEu sou o chatbot não-'
                            'oficial de dúvidas da UACSA/UFRPE \U0001F601 \n. '
                            'Todas as mensagens enviadas para mim serão '
                            'gravadas para, no futuro, melhorarmos as minhas '
                            'respostas. Em que posso ajudar?'}
        return create_answer(texto_recebido)
    else:
        return {'text': f'Desculpe, só processo mensagens de texto por '
                        f'enquanto \U00002639'}


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


def send_photo(photo_adress, body, caption=None):
    if app.config['ENV'] == 'development':
        print('\n [ENVIANDO IMAGEM]:', photo_adress, '\n')
    else:
        # a imagem precisa estar no servidor, não funciona para url
        if caption is None:
            with open(os.path.join(script_dir, photo_adress), 'rb') as photo:
                endpoint = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
                params = {
                    "chat_id": body['message']['chat']['id']
                }
                get(endpoint, params, files={'photo': photo})
        else:
            with open(os.path.join(script_dir, photo_adress), 'rb') as photo:
                endpoint = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
                params = {
                    "chat_id": body['message']['chat']['id'],
                    "caption": caption
                }
                get(endpoint, params, files={'photo': photo})


def send_document(document_adress, body, caption=None):
    if app.config['ENV'] == 'development':
        print('\n [ENVIANDO DOCUMENTO]:', document_adress, '\n')
    else:
        if caption is None:
            with open(os.path.join(script_dir, document_adress), 'rb') as document:
                endpoint = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
                params = {
                    "chat_id": body['message']['chat']['id']
                }
                get(endpoint, params, files={'document': document})
        else:
            with open(os.path.join(script_dir, document_adress), 'rb') as document:
                endpoint = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
                params = {
                    "chat_id": body['message']['chat']['id'],
                    "caption": caption
                }
                get(endpoint, params, files={'document': document})
