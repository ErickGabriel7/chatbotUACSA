import os
import random

import yaml

from chatbotUACSA.utils import clean_text

script_dir = os.path.dirname(__file__)  # this is the absolute folder where this script is in


def load_intents():
    with open(os.path.join(script_dir, 'data/intents.yaml'), encoding='utf-8') as file:
        return yaml.load(file, yaml.SafeLoader)


def load_responses():
    with open(os.path.join(script_dir, 'data/responses.yaml'), encoding='utf-8') as file:
        return yaml.load(file, yaml.SafeLoader)


intents = load_intents()
responses = load_responses()


def evaluate_intent(text):
    for intent, content in intents.items():
        for utterance in content['utterances']:
            # If the utterance has a + symbol it means that it has multiple AND terms.
            # Otherwise, a simple check will suffice.
            if '+' in utterance:
                terms = utterance.split('+')
                if all(term in text for term in terms):
                    return intent
            elif utterance in text:
                return intent
    return None


def respond_intent(command):
    global there_is_img
    global there_is_text
    global there_is_doc
    result = None
    try:
        if responses[command] is not None and responses[command]['responses'] is not None:
            try:
                if responses[command]['responses']['text'] is not None:
                    there_is_text = True
            except KeyError:
                there_is_text = False
            try:
                if responses[command]['responses']['images'] is not None:
                    there_is_img = True
            except KeyError:
                there_is_img = False
            try:
                if responses[command]['responses']['docs'] is not None:
                    there_is_doc = True
            except KeyError:
                there_is_doc = False
            if there_is_text:
                if there_is_img:
                    if there_is_doc:
                        result = {'text': random.choice(responses[command]['responses']['text']),
                                  'images': random.choice(responses[command]['responses']['images']),
                                  'docs': random.choice(responses[command]['responses']['docs'])
                                  }
                    else:
                        result = {'text': random.choice(responses[command]['responses']['text']),
                                  'images': random.choice(responses[command]['responses']['images'])
                                  }
                else:
                    if there_is_doc:
                        result = {'text': random.choice(responses[command]['responses']['text']),
                                  'docs': random.choice(responses[command]['responses']['docs'])
                                  }
                    else:
                        result = {'text': random.choice(responses[command]['responses']['text'])}
            elif there_is_doc:
                result = {'docs': random.choice(responses[command]['responses']['docs'])}
            else:
                if there_is_img:
                    if there_is_doc:
                        result = {'docs': random.choice(responses[command]['responses']['docs']),
                                  'images': random.choice(responses[command]['responses']['images'])
                                  }
                    else:
                        result = {'images': random.choice(responses[command]['responses']['images'])
                                  }

    except KeyError:
        result = 'Hmm, eu acho que entendi o que você quer, mas ainda não sei responder isso.' \
                 '\nAtualmente só posso ajudar com comprovantes ' \
                 'de matrícula, declaração de vínculo, dispensas, estágio e desligamento.'

    return result


if __name__ == '__main__':
    # Load intents and responses from files

    print('Olá, eu sou o bot da uacsa!')

    while True:
        text = clean_text(input('O que você deseja? '))

        intent = evaluate_intent(text)
        if intent is None:
            print('puxa acho que entendi mais ainda não sei responder.\nAtualmente só posso ajudar com comprovantes '
                  'de matrícula, declaração de vínculo, dispensas, estágio e desligamento. ')
        else:
            command_result = respond_intent(intent)
            print(command_result)
