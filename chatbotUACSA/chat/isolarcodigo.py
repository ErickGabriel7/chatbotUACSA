import yaml
import random
from chatbotUACSA.utils import clean_text


def load_intents():
    with open('intents.yaml', encoding='utf-8') as file:
        return yaml.load(file, yaml.SafeLoader)


def load_responses():
    with open('responses.yaml', encoding='utf-8') as file:
        return yaml.load(file, yaml.SafeLoader)


intents = load_intents()
responses = load_responses()


def evaluate_intent(text):
    for intent, content in intents.items():
        for utterance in content['utterances']:
            # If the utterance has a + symbols it means that it has multiple AND terms.
            # Otherwise, a simple check will suffice.
            if '+' in utterance:
                terms = utterance.split('+')
                if all(term in text for term in terms):
                    return intent
            elif utterance in text:
                return intent

    return None


def respond_intent(command):
    result = None

    try:
        if responses[command] != None and responses[command]['responses'] != None:
            result = random.choice(responses[command]['responses'])
    except KeyError:
        result = 'Hm, eu acho que entendi o que você quer, mas ainda não sei responder isso.'

    return result


if __name__ == '__main__':
    # Load intents and responses from files

    print('Olá, eu sou o bot da uacsa!')

    while True:
        text = clean_text(input('O que você deseja? '))

        intent = evaluate_intent(text)
        if intent is None:
            print(
                'puxa acho que entendi mais ainda não sei responder.\nAtualmente só posso ajudar com comprovantes de matrícula,declaração de vínculo,dispensas,estágio e desligamento. ')
        else:
            command_result = respond_intent(intent)
            print(command_result)
