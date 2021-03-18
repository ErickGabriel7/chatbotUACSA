from chatbotUACSA.utils import clean_text
from chatbotUACSA.chat.data_loading import load_intents, load_responses, evaluate_intent, respond_intent


def create_answer(input_text):
    input_text = clean_text(input_text)
    ok = evaluate_intent(input_text)
    if ok is None:
        print(
            'puxa acho que entendi mais ainda não sei responder.\nAtualmente só posso ajudar com comprovantes,dispensas,estágio e desligamento. ')
    else:
        response = respond_intent(ok)
        print('Resposta:', response)
