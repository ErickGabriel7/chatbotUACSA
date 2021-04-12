import unittest
import chatbotUACSA.chat.data_loading as data_loading

def get_responses(examples):
    responses = []
    for example in examples:
        responses.append(data_loading.evaluate_intent(example))
    return responses

class TestIntents(unittest.TestCase):
    """This suit evaluates if example utterances are being matched to
    the correct intents"""


    def test_idesligamento(self):
        expected = 'i_desligamento'
        examples = [
            'posso ser expulsa da universidade?',
            'como funciona o desligamento?',
            'não quero ser desligado',
            'é possível ser jubilado?',
            'o que é a COAA?',
        ]

        self.assertSequenceEqual([expected]*len(examples), get_responses(examples))
