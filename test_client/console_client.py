import chatbotUACSA.chat.processing as processing

if __name__ == '__main__':
    print('Iniciando interação com o chatbot')
    print('Para sair digite \q')
    text = ''
    while text != '\q':
        text = input('Você: ')
        response = processing.create_answer(text, 'username')
        print('Resposta:', response)
