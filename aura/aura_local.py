class AuraLocal:
    def __init__(self, core):
        self.core = core

    def start(self):
        print("AURA Local ready.")
        while True:
            cmd = input(">> ")
            print(self.core.execute(cmd))
