from modules.nlp.nlp_main import NLPModule
from modules.file.file_main import FileModule
from modules.security.security_main import SecurityModule
from modules.ui.ui_main import UIModule
from modules.autodev.autodev_main import AutoDevModule

class CommandRouter:
    def __init__(self, core):
        self.core = core
        self.modules = {
            "nlp": NLPModule(),
            "file": FileModule(),
            "security": SecurityModule(),
            "ui": UIModule(),
            "autodev": AutoDevModule()
        }

    def route(self, command: str):
        if command.startswith("nlp."):
            return self.modules["nlp"].handle(command)
        if command.startswith("file."):
            return self.modules["file"].handle(command)
        if command.startswith("security."):
            return self.modules["security"].handle(command)
        if command.startswith("ui."):
            return self.modules["ui"].handle(command)
        if command.startswith("autodev."):
            return self.modules["autodev"].handle(command)

        return "Unknown command."
