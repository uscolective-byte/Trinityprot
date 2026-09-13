import os

class FileOps:
    def execute(self, command: str):
        if "file.read" in command:
            path = command.split("=")[1]
            return open(path).read()
        if "file.write" in command:
            _, path, text = command.split("|")
            with open(path, "w") as f:
                f.write(text)
            return "File written."
        return "Unknown file operation."
