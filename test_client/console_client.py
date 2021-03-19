from chatbotUACSA.chat.processing import create_answer

text = ""
while text != 'sair':
    text = input("você: ")
    resposta = create_answer(text)
    print(resposta)
