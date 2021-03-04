import requests
import json

target_URL = "http://127.0.0.1:5000/nova-mensagem"
parameters = {
    "update_id": "955434638",
    "message": {
        "message_id": "69",
        "from": {
            "id": "778176063",
            "is_bot": "false",
            "first_name": "Erick",
            "last_name": "Gabriel",
            "language_code": "pt-br"
        },
        "chat": {
            "id": "778176063",
            "first_name": "Erick",
            "last_name": "Gabriel",
            "type": "private"
        },
        "date": "1614793386",
        "text": "Oi"
    }
}

if __name__ == '__main__':
    print('Iniciando interação com o chatbot')
    print('Para sair digite \q')
    text = ''
    while text != '\q':
        text = input('Você: ')
        parameters['message']['text'] = text
        response = requests.post(target_URL, json=parameters)
        print('Resposta:', response)
