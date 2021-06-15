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
        app.logger.debug('Updated PythonAnywhere successfully')
        return 'Updated PythonAnywhere successfully', 200
    else:
        app.logger.debug('Wrong event type')
        return 'Wrong event type', 400


def send_answer(resposta, body):
    # Função que processa a resposta gerada e escolhe que tipo de função de envio usar.
    global there_is_img
    global there_is_text
    global there_is_doc
    texto_recebido = body['message']['text']
    try:
        intent = resposta['intent']
    except TypeError:
        intent = 'None'
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

                if len(resposta_texto) > 1024:
                    app.logger.info(
                        f"Texto Recebido: {texto_recebido} \nIntent: {intent}\nResposta (send_photo, send_document e send_text_message): {resposta_texto}\nArquivo de imagem: {resposta_imagem}\nDocumento: {resposta_documento}")
                    send_text_message(resposta_texto, body)
                    send_photo(resposta_imagem, body)
                    send_document(resposta_documento, body)
                else:
                    app.logger.info(
                        f"Texto Recebido: {texto_recebido} \nIntent: {intent}\nResposta (send_photo e send_document, caption=True): {resposta_imagem}\nDocumento: {resposta_documento}")
                    send_photo(resposta_imagem, body, caption=resposta_texto)
                    send_document(resposta_documento, body)

            else:
                resposta_imagem = resposta['images']
                resposta_texto = resposta['text']

                if len(resposta_texto) > 1024:
                    app.logger.info(
                        f"Texto Recebido: {texto_recebido} \nIntent: {intent}\nResposta (send_photo e send_text_message): {resposta_texto}\nArquivo de Imagem: {resposta_imagem}")
                    send_text_message(resposta_texto, body)
                    send_photo(resposta_imagem, body)
                else:
                    app.logger.info(
                        f"Texto Recebido: {texto_recebido} \nIntent: {intent}\nResposta (send_photo, caption=True): {resposta_texto}\nArquivo de Imagem: {resposta_imagem}")
                    send_photo(resposta_imagem, body, caption=resposta_texto)
        else:
            if there_is_doc:
                resposta_documento = resposta['docs']
                resposta_texto = resposta['text']

                if len(resposta_texto) > 1024:
                    app.logger.info(
                        f"Texto Recebido: {texto_recebido} \nIntent: {intent}\nResposta (send_document e send_text_message): {resposta_texto}\nDocumento: {resposta_documento}")
                    send_text_message(resposta_texto, body)
                    send_document(resposta_documento, body)
                else:
                    app.logger.info(
                        f"Texto Recebido: {texto_recebido} \nIntent: {intent}\nResposta (send_document, caption=True): {resposta_texto}\nDocumento: {resposta_documento}")
                    send_document(resposta_documento, body, caption=resposta_texto)
            else:
                resposta = resposta['text']

                app.logger.info(
                    f"Texto Recebido: {texto_recebido} \nIntent: {intent}\nResposta (send_text_message): {resposta}")
                send_text_message(resposta, body)
    elif there_is_doc:
        resposta_documento = resposta['docs']

        app.logger.info(
            f"Texto Recebido: {texto_recebido} \nIntent: {intent}\nResposta (send_document): {resposta}")
        send_document(resposta_documento, body)
    else:
        if there_is_img:
            if there_is_doc:
                resposta_documento = resposta['docs']
                resposta_imagem = resposta['images']

                app.logger.info(
                    f"Texto Recebido: {texto_recebido} \nIntent: {intent}\nResposta (send_photo e send_document): {resposta_imagem}\nDocumento: {resposta_documento}")
                send_photo(resposta_imagem, body)
                send_document(resposta_documento, body)
            else:
                resposta_imagem = resposta['images']

                app.logger.info(
                    f"Texto Recebido: {texto_recebido} \nIntent: {intent}\nResposta (send_photo): {resposta}")
                send_photo(resposta_imagem, body)

    pass


def process_message(body):
    mensagem_erro = {'text': f'Desculpe, só processo mensagens de texto por '
                             f'enquanto \U00002639',
                     'intent': 'None'}
    # verificando se a mensagem é um texto
    try:
        if 'text' in body['message']:
            texto_recebido = body['message']['text']
            nome_usuario = body['message']['from']['first_name']
            # quando um novo usuário inicia uma conversa com o bot, a primeira mensagem é sempre '\start'
            if texto_recebido == '/start':
                return {'text': f'Olá, {nome_usuario}!\nEu sou o chatbot não-'
                                'oficial para tirar dúvidas dos estudantes da UACSA/UFRPE \U0001F601 \n. '
                                'Todas as mensagens enviadas para mim serão '
                                'gravadas para, no futuro, melhorarmos as minhas '
                                'respostas. Em que posso ajudar?',
                        'intent': 'None'}
            return create_answer(texto_recebido)
        else:
            return mensagem_erro
    except KeyError:
        return mensagem_erro


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
    photo_adress = 'data/img/' + photo_adress

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
    document_adress = 'data/doc/' + document_adress

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
