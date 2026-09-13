class SecurityEngine:
    def check(self, command: str):
        blocked = ["rm -rf", "delete_system", "format_disk"]
        return not any(b in command for b in blocked)
