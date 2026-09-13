class Logger:
    def log(self, text: str):
        with open("trinity.log", "a") as f:
            f.write(text + "\n")
