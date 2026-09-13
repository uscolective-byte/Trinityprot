from core.command_router import CommandRouter
from core.state_manager import StateManager
from core.security_engine import SecurityEngine
from core.logger import Logger

class TrinityCore:
    def __init__(self):
        self.state = StateManager()
        self.security = SecurityEngine()
        self.logger = Logger()
        self.router = CommandRouter(self)

    def execute(self, command: str):
        self.logger.log(f"Received command: {command}")

        if not self.security.check(command):
            return "SECURITY BLOCK: Command denied."

        result = self.router.route(command)
        self.logger.log(f"Result: {result}")
        return result
