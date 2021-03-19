from chatbotUACSA.utils import clean_text
from .data_loading import evaluate_intent, respond_intent


def create_answer(input_text):
    input_text = clean_text(input_text)
    ok = evaluate_intent(input_text)
    if ok is None:
        return (
            'puxa acho que entendi mais ainda não sei responder.\nAtualmente só posso ajudar com comprovantes,dispensas,estágio e desligamento. ')
    else:
        response = respond_intent(ok)
        return ('Resposta:', response)
