import os

class ProjectBuilder:
    def create(self, name: str):
        os.makedirs(name, exist_ok=True)
        return f"Project '{name}' created."
