class IntentParser:
    def parse(self, command: str):
        return command.replace("nlp.", "")
