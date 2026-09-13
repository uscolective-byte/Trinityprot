import fs from "fs";
import path from "path";

// Asimilované z oficiálneho dokumentu: 10 ZÁKONOV TRINITY
export const TRINITY_LAWS = [
  "1. Jadro musí mať absolútnu kontrolu nad všetkými modulmi, procesmi a dátovými tokmi.",
  "2. Žiadny modul nesmie vykonať operáciu mimo povoleného rozsahu (bezpečnosť je na prvom mieste).",
  "3. Systém musí byť autonómny, rásť, meniť sa a prispôsobovať sa bez externých zásahov.",
  "4. Komunikácia medzi používateľom a systémom musí byť čistá, presná a bezpečná.",
  "5. Každý príkaz musí byť analyzovaný, kontrolovaný a vykonaný presne tak, ako má.",
  "6. Každý modul musí byť izolovaný, aby sa zabránilo nebezpečným operáciám (Sandboxing).",
  "7. Systém musí byť rozšíriteľný, integrovať nové moduly a technológie.",
  "8. Logovanie je povinné a každá operácia musí byť zaznamenaná.",
  "9. AURA je jediný komunikačný kanál medzi človekom a systémom.",
  "10. Jadro musí vždy chrániť stabilitu systému, bez ohľadu na okolnosti."
];

export interface ValidationResult {
  allowed: boolean;
  reason?: string;
  violatedLaw?: number;
}

export class TrinityConstitution {
  private secureZones: string[] = ["/generated_apps", "/data", "/logs", "/memory"];
  private blockedKeywords: string[] = ["rm -rf /", "drop database", "chmod 777", "process.exit"];

  constructor() {
    this.logSystemEvent("Ústava TRINITY inicializovaná. 10 Zákony sú aktívne.");
  }

  // ZÁKON #8: Logovanie je povinné
  private logSystemEvent(message: string) {
    const logDir = path.join(process.cwd(), "logs");
    if (!fs.existsSync(logDir)) fs.mkdirSync(logDir, { recursive: true });
    const logMessage = `[${new Date().toISOString()}] [CONSTITUTION] ${message}\n`;
    fs.appendFileSync(path.join(logDir, "security.log"), logMessage);
  }

  public validateAction(actionContext: string, requestedPath?: string): ValidationResult {
    const actionLower = actionContext.toLowerCase();

    // ZÁKON #2 & #10: Ochrana pred nebezpečnými operáciami a stabilita
    for (const keyword of this.blockedKeywords) {
      if (actionLower.includes(keyword)) {
        this.logSystemEvent(`BLOCKED: Detegovaný zakázaný príkaz: ${keyword}`);
        return { allowed: false, reason: "Kritické ohrozenie stability systému.", violatedLaw: 10 };
      }
    }

    // ZÁKON #6: Izolácia a Sandboxing
    if (requestedPath) {
      const isSafeZone = this.secureZones.some(zone => requestedPath.includes(zone));
      if (!isSafeZone) {
        this.logSystemEvent(`BLOCKED: Pokus o zápis mimo sandboxu: ${requestedPath}`);
        return { allowed: false, reason: "Operácia mimo povolenej bezpečnej zóny.", violatedLaw: 6 };
      }
    }

    this.logSystemEvent(`APPROVED: Akcia [${actionContext}] prešla kontrolou Ústavy.`);
    return { allowed: true };
  }
}

// Export pre priame použitie v orchestrátore
const constitutionGuard = new TrinityConstitution();
export const validateActionAgainstConstitution = (actionContext: string, targetPath?: string) => 
  constitutionGuard.validateAction(actionContext, targetPath);
