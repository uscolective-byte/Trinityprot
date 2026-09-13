from modules.autodev.code_generator import CodeGenerator
from modules.autodev.version_manager import VersionManager

class AutoDevModule:
    def __init__(self):
        self.gen = CodeGenerator()
        self.ver = VersionManager()

    def handle(self, command: str):
        if "autodev.gen" in command:
            return self.gen.generate()
        return self.ver.version()
