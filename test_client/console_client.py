from chatbotUACSA.chat.processing import create_answer

text = ""
while text != 'sair':
    text = input("você: ")
    resposta = create_answer(text)
    print(resposta['text'])
    if 'images' in resposta:
        print('  --IMAGEN(S):', resposta['images'])
    if 'docs' in resposta:
        print('  --ARQUIVO(S):', resposta['docs'])
