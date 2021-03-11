from chatbotUACSA.chat.isolarcodigo import load_intents, load_responses, evaluate_intent, respond_intent
import random

if __name__ == '__main__':
    available_intents = load_intents()
    available_responses = load_responses()

    random.seed()  # Prepare random number generation

    print('Iniciando interação com o chatbot')
    print('Para sair digite \q')
    text = ''
    while text != '\q':
        text = input('Você: ')
        intent = evaluate_intent(text, available_intents)
        if intent is None:
            print('puxa acho que entendi mais ainda não sei responder.\nAtualmente só posso ajudar com comprovantes,dispensas,estágio e desligamento. ')
        else:
            response = respond_intent(intent, available_responses)
            print('Resposta:', response)
