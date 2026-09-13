from modules.nlp.intent_parser import IntentParser
from modules.nlp.text_generator import TextGenerator

class NLPModule:
    def __init__(self):
        self.parser = IntentParser()
        self.generator = TextGenerator()

    def handle(self, command: str):
        intent = self.parser.parse(command)
        return self.generator.generate(intent)
