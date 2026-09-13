from core.core_main import TrinityCore
from aura.aura_local import AuraLocal

if __name__ == "__main__":
    core = TrinityCore()
    aura = AuraLocal(core)
    aura.start()
