from chatbotUACSA.utils import clean_text
from .data_loading import evaluate_intent, respond_intent


def create_answer(input_text):
    input_text = clean_text(input_text)
    intent = evaluate_intent(input_text)
    if intent is None:
        return {'text': 'Puxa, ainda não sei te informar sobre isso. '
                        'Atualmente só posso ajudar com informações sobre '
                        'comprovantes, estágio, desligamento, calendário e '
                        'dispensa de disciplinas.',
                'intent': 'None'}
    else:
        response = respond_intent(intent)
        return response
