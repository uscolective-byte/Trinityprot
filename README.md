# TRINITY OMNI-CORE

TRINITY OMNI-CORE je pokročilý, autonómny, multi-agentový riadiaci systém umelej inteligencie postavený na architektúre Google Agent Development Kit (ADK) a modeli `gemini-3.5-flash`. Systém funguje ako centrálny mozog (orchestrátor), ktorý prepája Python backend s moderným Next.js rozhraním a riadi šesť špecializovaných sub-agentov pre vývoj, bezpečnosť, DevOps, databázy, výskum a QA testovanie.

---

## 🏗️ Architektúra Systému

Architektúra je navrhnutá s dôrazom na modularitu, bezpečnosť a úplnú autonómiu pri spracovaní úloh:

*   **TRINITY Core (Root Orchestrator):** Centrálna riadiaca jednotka, ktorá prijíma príkazy, spúšťa autonómnu ReAct slučku uvažovania a deleguje úlohy na príslušné sub-moduly.
*   **AURA Interface:** Komunikačná vrstva (Next.js dashboard a REST API), ktorá zabezpečuje vizualizáciu telemetrie v reálnom čase a prekladá používateľské príkazy.
*   **Ústava (Constitution):** Bezpečnostný mechanizmus a sandboxing, ktorý validuje každú akciu (zápis na disk, spustenie procesu) pred jej fyzickým vykonaním.

---

## 🤖 Hierarchia 6 Sub-Agentov

1.  **`app_builder_agent`** – Generuje kompletné multi-file štruktúry, full-stack aplikačný kód (Flask, Node.js) a zabezpečuje fyzický I/O zápis na disk.
2.  **`devops_deploy_agent`** – Špecializuje sa na Git workflowy, CI/CD pipelines, Docker kontajnery a cloudové konfigurácie.
3.  **`research_agent`** – Využíva nástroje Google Search a URL Context na rešerš dokumentácie a overovanie API v reálnom čase.
4.  **`security_audit_agent`** – Vykonáva bezpečnostný audit kódu, kontroluje prístupové práva a zabezpečuje dodržiavanie Ústavy.
5.  **`qa_test_agent`** – Generuje robustné testovacie suity, E2E validácie a rieši ladiace procedúry.
6.  **`database_architect`** – Navrhuje SQL/NoSQL schémy, optimalizuje queries a vytvára bezpečné databázové migrácie.

---

## 📁 Štruktúra Projektu

```text
trinity-omni-core/
├── package.json
├── requirements.txt
├── tsconfig.json
├── tailwind.config.ts
├── postcss.config.js
├── Dockerfile
├── docker-compose.yml
├── setup.sh
├── agent_engine/
│   ├── __init__.py
│   ├── main.py
│   ├── agents.py
│   └── constitution.py
├── app/
│   ├── globals.css
│   ├── layout.tsx
│   ├── page.tsx          # Vstupná Homepage
│   ├── dashboard/
│   │   └── page.tsx      # AURA Riadiaca Konzola
│   └── api/
│       ├── agent/
│       │   └── route.ts
│       ├── builder/
│       │   └── route.ts
│       └── skills/
│           └── route.ts
├── core/
│   ├── constitution.ts
│   ├── orchestrator.ts
│   └── types.ts
├── skills/
│   ├── appBuilder.ts
│   ├── dynamicEngine.ts
│   └── registry.ts
└── memory/
    └── engine.ts
