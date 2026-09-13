from modules.file.file_ops import FileOps
from modules.file.project_builder import ProjectBuilder

class FileModule:
    def __init__(self):
        self.ops = FileOps()
        self.builder = ProjectBuilder()

    def handle(self, command: str):
        if "create_project" in command:
            name = command.split("=")[1]
            return self.builder.create(name)
        return self.ops.execute(command)
