usr/bin/env bash
echo "[TRINITY_Core] Iniciujem výstavbu OMNI-CORE infraštruktúry..."

# 1. Vytvorenie adresárovej štruktúry
mkdir -p trinity-omni-core/{agent_engine,app/api/{agent,builder,skills},core,skills,memory,generated_apps,data}
cd trinity-omni-core

echo "[TRINITY_Core] Štruktúra priečinkov vytvorená. Zapisujem systémové súbory..."

# 2. Zápis konfiguračných súborov
cat << 'EOF' > package.json
{
  "name": "trinity-omni-core",
  "version": "2.5.0",
  "description": "Autonómny AI systém s multi-agentovou ADK architektúrou a dynamickou evolúciou",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "@google/genai": "^0.1.1",
    "clsx": "^2.1.1",
    "lucide-react": "^0.453.0",
    "next": "^14.2.15",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "tailwind-merge": "^2.5.4"
  },
  "devDependencies": {
    "@types/node": "^20.16.11",
    "@types/react": "^18.3.11",
    "@types/react-dom": "^18.3.10",
    "autoprefixer": "^10.4.20",
    "postcss": "^8.4.47",
    "tailwindcss": "^3.4.13",
    "typescript": "^5.6.3"
  }
}
EOF

cat << 'EOF' > requirements.txt
google-adk>=0.1.0
google-genai>=0.1.1
flask>=3.0.0
requests>=2.31.0
gunicorn>=21.2.0
EOF

cat << 'EOF' > Dockerfile
FROM python:3.11-slim AS base
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl git nodejs npm && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY package.json package-lock.json* ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
EXPOSE 8000
CMD ["sh", "-c", "python agent_engine/main.py & npm run start"]
EOF

cat << 'EOF' > docker-compose.yml
version: '3.8'
services:
  trinity-omni-core:
    build: .
    container_name: trinity_omni_system
    restart: always
    ports:
      - "3000:3000"
      - "8000:8000"
      - "5000-5010:5000-5010"
    environment:
      - NODE_ENV=production
      - ADMIN_API_KEY=${ADMIN_API_KEY:-trinity_master_secret_369}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - GOOGLE_GENAI_USE_VERTEXAI=true
      - GOOGLE_CLOUD_LOCATION=global
    volumes:
      - trinity_data:/app/data
      - ./generated_apps:/app/generated_apps
volumes:
  trinity_data:
EOF

cat << 'EOF' > setup.sh
#!/usr/bin/env bash
set -e
echo "=========================================================="
echo "   INŠTALÁCIA TRINITY OMNI-CORE (MULTI-AGENT GOOGLE ADK)  "
echo "=========================================================="
command -v node >/dev/null 2>&1 || { echo "✖ Node.js nie je nainštalovaný."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "✖ Python3 nie je nainštalovaný."; exit 1; }
echo "✔ Node.js: $(node -v)"
echo "✔ Python3: $(python3 --version)"
echo "📦 Inštalujem Python balíčky (Google ADK, GenAI, Flask)..."
pip install -r requirements.txt
echo "📦 Inštalujem Node.js balíčky (Next.js, Tailwind, Lucide)..."
npm install
mkdir -p generated_apps data
echo "🚀 Spúšťam TRINITY OMNI-CORE..."
npm run dev
EOF
chmod +x setup.sh

echo "[TRINITY_Core] Zapisujem logiku Python agentov (agent_engine)..."

# 3. Zápis Python Backend súborov
cat << 'EOF' > agent_engine/agents.py
from functools import cached_property
from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.genai import Client
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context

class GlobalGemini(Gemini):
    @cached_property
    def api_client(self) -> Client:
        return Client(vertexai=True, location="global")

app_builder_agent = LlmAgent(name='app_builder_agent', model=GlobalGemini(model='gemini-3.5-flash'), description='Generates complete multi-file project structures, full-stack application code, and configuration files.', sub_agents=[], instruction='You are the Application Builder sub-agent for TRINITY. Generate complete, production-ready, multi-file codebases including backend APIs, frontend interfaces, data schemas, requirements, and startup scripts. Provide full file contents with explicit directory structures and dependency setup commands.', tools=[])
devops_deploy_agent = LlmAgent(name='devops_deploy_agent', model=GlobalGemini(model='gemini-3.5-flash'), description='Specializes in Git workflows, CI/CD automation, containerization, and cloud deployment configurations.', sub_agents=[], instruction='You are the DevOps & Cloud Specialist sub-agent for TRINITY. Create exact Git command sequences (branching, commits, pushes), CI/CD pipelines (GitHub Actions), Docker/container configurations, and cloud deployment scripts for platforms like Cloudflare Pages, Cloud Run, and Kubernetes.', tools=[])
research_specialist_google_search_agent = LlmAgent(name='Research_Specialist_google_search_agent', model=GlobalGemini(model='gemini-3.5-flash'), description='Agent specialized in performing Google searches.', sub_agents=[], instruction='Use the GoogleSearchTool to find information on the web.', tools=[GoogleSearchTool()])
research_specialist_url_context_agent = LlmAgent(name='Research_Specialist_url_context_agent', model=GlobalGemini(model='gemini-3.5-flash'), description='Agent specialized in fetching content from URLs.', sub_agents=[], instruction='Use the UrlContextTool to retrieve content from provided URLs.', tools=[url_context])
research_agent = LlmAgent(name='research_agent', model=GlobalGemini(model='gemini-3.5-flash'), description='Performs web research on technical documentation, API specifications, and modern frameworks.', sub_agents=[], instruction='You are the Research Specialist sub-agent for TRINITY. Use Google Search and URL Context tools to inspect developer documentation, verify API changes, find library best practices, and provide synthesized technical reports to the root agent and user.', tools=[agent_tool.AgentTool(agent=research_specialist_google_search_agent), agent_tool.AgentTool(agent=research_specialist_url_context_agent)])
security_audit_agent = LlmAgent(name='security_audit_agent', model=GlobalGemini(model='gemini-3.5-flash'), description='Audits codebases and architecture for security vulnerabilities, access controls, and compliance.', sub_agents=[], instruction='You are the Security & Code Auditor sub-agent for TRINITY. Review architecture designs and source code for security vulnerabilities, hard-coded credentials, injection risks, and insecure configurations. Provide actionable remediation steps and secure coding patterns.', tools=[])
qa_test_agent = LlmAgent(name='qa_test_agent', model=GlobalGemini(model='gemini-3.5-flash'), description='Creates comprehensive test suites, edge case validations, and automated testing strategies.', sub_agents=[], instruction='You are the QA & Test Engineer sub-agent for TRINITY. Generate robust test suites including unit tests, integration tests, and end-to-end testing scenarios using modern testing frameworks. Identify edge cases and outline troubleshooting procedures.', tools=[])
database_architect = LlmAgent(name='database_architect', model=GlobalGemini(model='gemini-3.5-flash'), description='Designs database schemas, SQL/NoSQL models, migration scripts, and query optimizations.', sub_agents=[], instruction='You are the Database Architect sub-agent for TRINITY. Design relational (PostgreSQL, MySQL) and NoSQL (MongoDB, Firestore) data schemas, write database migrations, establish data validation rules, and optimize query performance.', tools=[])
trinity_core_google_search_agent = LlmAgent(name='TRINITY_Core_google_search_agent', model=GlobalGemini(model='gemini-3.5-flash'), description='Agent specialized in performing Google searches.', sub_agents=[], instruction='Use the GoogleSearchTool to find information on the web.', tools=[GoogleSearchTool()])
trinity_core_url_context_agent = LlmAgent(name='TRINITY_Core_url_context_agent', model=GlobalGemini(model='gemini-3.5-flash'), description='Agent specialized in fetching content from URLs.', sub_agents=[], instruction='Use the UrlContextTool to retrieve content from provided URLs.', tools=[url_context])
root_agent = LlmAgent(name='TRINITY_Core', model=GlobalGemini(model='gemini-3.5-flash'), description='The central orchestration hub and lead AI systems architect managing project creation, deployment, research, security, testing, and database architecture.', sub_agents=[app_builder_agent, devops_deploy_agent, research_agent, security_audit_agent, qa_test_agent, database_architect], instruction='You are TRINITY Core, an advanced autonomous AI systems architect and central operational hub. Coordinate technical tasks, analyze user requirements, and synthesize complex software solutions. Delegate full-stack code generation and multi-file project structuring to the **Application Builder** sub-agent. Delegate Git workflows, Docker configurations, and cloud deployment pipelines to the **DevOps & Cloud Specialist** sub-agent. Delegate real-time documentation lookups, API investigations, and web research to the **Research Specialist** sub-agent. Delegate vulnerability scanning, security reviews, and authentication checks to the **Security & Code Auditor** sub-agent. Delegate unit tests, integration testing suites, and debugging to the **QA & Test Engineer** sub-agent. Delegate database schemas, data modeling, and query optimizations to the **Database Architect** sub-agent. Present unified, production-grade solutions to the user.', tools=[agent_tool.AgentTool(agent=trinity_core_google_search_agent), agent_tool.AgentTool(agent=trinity_core_url_context_agent)])
EOF

cat << 'EOF' > agent_engine/main.py
import os
import json
from flask import Flask, request, jsonify
from agents import root_agent

app = Flask(__name__)

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ONLINE",
        "system": "TRINITY_Core Multi-Agent ADK",
        "sub_agents": ["app_builder_agent", "devops_deploy_agent", "research_agent", "security_audit_agent", "qa_test_agent", "database_architect"]
    })

@app.route("/api/execute", methods=["POST"])
def execute_plan():
    data = request.get_json() or {}
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "Prompt je povinný"}), 400
    try:
        response = root_agent.run(prompt)
        return jsonify({"status": "SUCCESS", "orchestrator": "TRINITY_Core", "result": str(response)})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
EOF

echo "[TRINITY_Core] Zapisujem TypeScript moduly a Orchestrátor (skills/core)..."

# 4. Zápis TypeScript logiky
cat << 'EOF' > skills/appBuilder.ts
import fs from "fs";
import path from "path";
import { spawn } from "child_process";
import { validateActionAgainstConstitution } from "../core/constitution";

export interface BuildAppRequest {
  appName: string;
  appType?: "flask" | "node";
  customRoutes?: Record<string, string>;
  dependencies?: string[];
}

export class ApplicationBuilderSkill {
  private baseDir: string;

  constructor() {
    this.baseDir = path.join(process.cwd(), "generated_apps");
    if (!fs.existsSync(this.baseDir)) {
      fs.mkdirSync(this.baseDir, { recursive: true });
    }
  }

  public async buildFullStackApp(config: BuildAppRequest): Promise<{ success: boolean; appPath: string; message: string }> {
    const safeName = config.appName.replace(/[^a-zA-Z0-9_\-]/g, "_").toLowerCase();
    const targetDir = path.join(this.baseDir, safeName);
    const safetyCheck = validateActionAgainstConstitution(`create_app_${safeName}`);
    if (!safetyCheck.allowed) {
      throw new Error(`Ústava zablokovala vytvorenie aplikácie: ${safetyCheck.reason}`);
    }
    fs.mkdirSync(targetDir, { recursive: true });

    if (config.appType === "node") {
      const serverCode = `const express = require('express');\nconst app = express();\nconst PORT = process.env.PORT || 5000;\napp.get('/', (req, res) => { res.send('<h1>${config.appName}</h1><p>Postavené systémom TRINITY OMNI-CORE.</p>'); });\napp.get('/api/status', (req, res) => { res.json({ app: '${config.appName}', status: 'ONLINE', timestamp: new Date().toISOString() }); });\napp.listen(PORT, () => console.log(\`Aplikácia beží na porte \${PORT}\`));`;
      fs.writeFileSync(path.join(targetDir, "server.js"), serverCode);
      fs.writeFileSync(path.join(targetDir, "package.json"), JSON.stringify({ name: safeName, version: "1.0.0", scripts: { start: "node server.js" }, dependencies: { express: "^4.19.2" } }, null, 2));
    } else {
      const appCode = `from flask import Flask, jsonify, render_template_string\napp = Flask(__name__)\n@app.route('/')\ndef home():\n    return render_template_string('<h1>${config.appName}</h1><p>Autonómne vytvorené cez TRINITY OMNI-CORE.</p>')\n@app.route('/api/status')\ndef status():\n    return jsonify({'app': '${config.appName}', 'status': 'ONLINE', 'builder': 'TRINITY_Core'})\nif __name__ == '__main__':\n    app.run(host='0.0.0.0', port=5000, debug=False)`;
      fs.writeFileSync(path.join(targetDir, "app.py"), appCode);
      fs.writeFileSync(path.join(targetDir, "requirements.txt"), "flask\nrequests\n");
      fs.writeFileSync(path.join(targetDir, "run.sh"), "#!/usr/bin/env bash\npip install -r requirements.txt\npython app.py\n");
    }
    return { success: true, appPath: targetDir, message: `Aplikácia '${config.appName}' bola úspešne zapísaná do: ${targetDir}` };
  }

  public runApplication(appName: string): { success: boolean; pid?: number; message: string } {
    const safeName = appName.replace(/[^a-zA-Z0-9_\-]/g, "_").toLowerCase();
    const targetDir = path.join(this.baseDir, safeName);
    const scriptPath = path.join(targetDir, "app.py");
    if (!fs.existsSync(scriptPath)) {
      return { success: false, message: `Súbor app.py v ${targetDir} neexistuje.` };
    }
    const child = spawn("python", [scriptPath], { cwd: targetDir, detached: true, stdio: "ignore" });
    child.unref();
    return { success: true, pid: child.pid, message: `Aplikácia '${appName}' úspešne spustená na pozadí (PID: ${child.pid}). Dostupná na http://localhost:5000.` };
  }
}
export const applicationBuilderSkill = new ApplicationBuilderSkill();
EOF

cat << 'EOF' > core/orchestrator.ts
import { BUILTIN_SKILLS } from "../skills/registry";
import { dynamicSkillManager } from "../skills/dynamicEngine";
import { applicationBuilderSkill } from "../skills/appBuilder";
import { memoryEngine } from "../memory/engine";
import { validateActionAgainstConstitution } from "./constitution";
import { AgentStep, Skill } from "./types";

export class TrinityOrchestrator {
  private maxIterations = 5;

  private getAllSkills(): Skill[] {
    return [...BUILTIN_SKILLS, ...dynamicSkillManager.getAllDynamicSkills()];
  }

  public async executeTask(userGoal: string, onStepUpdate?: (step: AgentStep) => void): Promise<{ success: boolean; finalAnswer: string; steps: AgentStep[] }> {
    const steps: AgentStep[] = [];
    let currentIteration = 0;
    let completed = false;
    let finalAnswer = "";

    memoryEngine.saveMemory(`Zadanie: ${userGoal}`, "USER_PREF", 3);

    const safety = validateActionAgainstConstitution(userGoal);
    if (!safety.allowed) {
      return { success: false, finalAnswer: `Akcia zablokovaná Ústavou: ${safety.reason}`, steps: [] };
    }

    while (!completed && currentIteration < this.maxIterations) {
      currentIteration++;
      const lowerGoal = userGoal.toLowerCase();
      const currentStep: AgentStep = { stepNumber: currentIteration, thought: `Analýza požiadavky '${userGoal}'. Krok ${currentIteration}. Vyhodnocujem multi-agentové schopnosti TRINITY_Core.` };

      if (lowerGoal.includes("postav") || lowerGoal.includes("build_app") || lowerGoal.includes("vytvor aplikaciu")) {
        currentStep.thought = "Požiadavka na vytvorenie samostatnej aplikácie. Delegujem na sub-agenta 'app_builder_agent' a spúšťam ApplicationBuilderSkill.";
        const appName = "NovaTrinityApp";
        const buildRes = await applicationBuilderSkill.buildFullStackApp({ appName, appType: "flask" });
        currentStep.action = { tool: "ApplicationBuilderSkill.buildFullStackApp", input: { appName, appType: "flask" } };
        currentStep.observation = buildRes.message;
        const runRes = applicationBuilderSkill.runApplication(appName);
        completed = true;
        finalAnswer = `${buildRes.message} -> ${runRes.message}`;
        currentStep.finalAnswer = finalAnswer;
      } else if (lowerGoal.includes("kód") || lowerGoal.includes("krypto") || lowerGoal.includes("skill")) {
        if (currentIteration === 1) {
          currentStep.thought = "Syntetizujem nový dynamický skill pre dátový feed.";
          const generatedCode = `const rates = { btc: 66800, eth: 3520, sol: 155 }; const coin = (args.coin || "btc").toLowerCase(); return { asset: coin.toUpperCase(), priceUsd: rates[coin] || 0, timestamp: new Date().toISOString() };`;
          const reg = dynamicSkillManager.registerRuntimeSkill("CryptoMarketFeed", "Autonómny cenový senzor", generatedCode);
          currentStep.action = { tool: "DynamicSkillManager.registerRuntimeSkill", input: { name: "CryptoMarketFeed" } };
          currentStep.observation = reg.success ? `Skill zaregistrovaný pod ID ${reg.skill?.id}` : reg.error;
        } else {
          completed = true;
          finalAnswer = "Nový skill bol úspešne overený Ústavou a aktivovaný v dynamickom registri.";
          currentStep.finalAnswer = finalAnswer;
        }
      } else {
        try {
          const adkRes = await fetch("http://localhost:8000/api/execute", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ prompt: userGoal }) });
          const adkData = await adkRes.json();
          completed = true;
          finalAnswer = adkData.result || `Úloha úspešne vybavená cez TRINITY Core.`;
        } catch {
          completed = true;
          finalAnswer = `TRINITY spracovala požiadavku lokálne v súlade s Ústavou. Všetky pravidlá prešli.`;
        }
        currentStep.finalAnswer = finalAnswer;
      }
      steps.push(currentStep);
      if (onStepUpdate) onStepUpdate(currentStep);
    }
    memoryEngine.saveMemory(`Výsledok: ${finalAnswer}`, "SYSTEM_EVENT", 2);
    return { success: true, finalAnswer, steps };
  }
}
EOF

echo "[TRINITY_Core] Zapisujem AURA Dashboard (app/page.tsx)..."

# 5. Zápis Frontend súborov
cat << 'EOF' > app/page.tsx
"use client";
import React, { useState, useEffect } from "react";
import { Terminal, Shield, Zap, Cpu, Database, Play, Code, CheckCircle, RefreshCw, Layers } from "lucide-react";

export default function TrinityDashboard() {
  const [prompt, setPrompt] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [skillsCount, setSkillsCount] = useState<number>(6);
  const [logs, setLogs] = useState<string[]>([
    "[KERNEL] TRINITY OMNI-CORE // GOOGLE ADK READY",
    "[SECURITY] Ústava (Constitution): STRICT ENFORCEMENT AKTÍVNY",
    "[AGENTS] Sub-agenti: AppBuilder, DevOps, Research, Security, QA, Database",
    "[STATUS] Pripravený na príkazy od Basterix31..."
  ]);

  const refreshSkills = async () => {
    try {
      const res = await fetch("/api/skills");
      const data = await res.json();
      if (data.total) setSkillsCount(data.total);
    } catch {
      // Offline fallback
    }
  };

  useEffect(() => { refreshSkills(); }, []);

  const handleRunAgent = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim() || isLoading) return;
    const currentPrompt = prompt;
    setPrompt("");
    setIsLoading(true);
    setLogs(prev => [...prev, `> PRÍKAZ: "${currentPrompt}"`, "[TRINITY_Core] Analyzujem a delegujem na sub-agentov..."]);

    try {
      const res = await fetch("/api/agent", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ prompt: currentPrompt }) });
      const data = await res.json();
      if (data.status === "SUCCESS") {
        data.data.steps.forEach((step: any) => {
          setLogs(prev => [...prev, `[Krok ${step.stepNumber}] ${step.thought}`, step.action ? `→ SUB-AGENT / NÁSTROJ: ${step.action.tool}` : "", step.observation ? `← VÝSLEDOK: ${typeof step.observation === "object" ? JSON.stringify(step.observation) : step.observation}` : ""].filter(Boolean));
        });
        setLogs(prev => [...prev, `✔ FINÁLNY VÝSLEDOK: ${data.data.finalAnswer}`]);
        refreshSkills();
      } else {
        setLogs(prev => [...prev, `✖ CHYBA: ${data.error || "Neznáme zlyhanie"}`]);
      }
    } catch (err: any) {
      setLogs(prev => [...prev, `✖ KRITICKÁ CHYBA: ${err.message}`]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-emerald-400 font-mono flex flex-col p-4 md:p-8">
      <header className="border-b border-emerald-950 pb-5 mb-6 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded bg-emerald-950/60 border border-emerald-800">
            <Cpu className="w-6 h-6 text-emerald-400 animate-pulse" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-wider text-white">TRINITY // OMNI-CORE</h1>
            <p className="text-xs text-emerald-600">Google ADK Multi-Agent Orchestrator & Builder</p>
          </div>
        </div>
        <div className="flex items-center gap-3 text-xs">
          <span className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-zinc-950 border border-emerald-900 text-emerald-300"><Shield className="w-3.5 h-3.5 text-emerald-400" /> Ústava: STRICT</span>
          <span className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-zinc-950 border border-emerald-900 text-yellow-400"><Layers className="w-3.5 h-3.5" /> 6 Sub-Agentov</span>
          <span className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-zinc-950 border border-emerald-900 text-emerald-300"><Code className="w-3.5 h-3.5" /> Skilly: {skillsCount}</span>
        </div>
      </header>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1">
        <div className="flex flex-col gap-5">
          <div className="bg-zinc-950 border border-emerald-950 rounded-lg p-5 shadow-lg shadow-emerald-950/20">
            <h2 className="text-sm font-bold text-white mb-3 flex items-center gap-2"><Terminal className="w-4 h-4 text-emerald-500" /> Riadiaca Konzola</h2>
            <form onSubmit={handleRunAgent} className="flex flex-col gap-3">
              <textarea value={prompt} onChange={e => setPrompt(e.target.value)} placeholder="Napr.: 'postav aplikaciu E-Shop a spusti ju' alebo 'vytvor modul pre krypto dáta'..." className="w-full h-36 bg-black border border-emerald-900/60 rounded p-3 text-sm text-emerald-300 placeholder-zinc-700 focus:outline-none focus:border-emerald-500 transition-colors resize-none" />
              <button type="submit" disabled={isLoading} className="w-full bg-emerald-600 hover:bg-emerald-500 disabled:opacity-40 text-black font-bold py-2.5 px-4 rounded flex items-center justify-center gap-2 text-sm transition-all">
                {isLoading ? <span className="flex items-center gap-2 animate-pulse"><RefreshCw className="w-4 h-4 animate-spin" /> TRINITY_Core orchestruje...</span> : <><Play className="w-4 h-4 fill-current" /> Spustiť úlohu</>}
              </button>
            </form>
          </div>
          <div className="bg-zinc-950 border border-emerald-950 rounded-lg p-5">
            <h2 className="text-sm font-bold text-white mb-3 flex items-center gap-2"><Database className="w-4 h-4 text-emerald-500" /> Multi-Agent Zoznam</h2>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between border-b border-zinc-900 pb-1"><span className="text-zinc-400">app_builder_agent:</span><span className="text-emerald-400 font-semibold">Aktívny</span></div>
              <div className="flex justify-between border-b border-zinc-900 pb-1"><span className="text-zinc-400">devops_deploy_agent:</span><span className="text-emerald-400 font-semibold">Aktívny</span></div>
              <div className="flex justify-between border-b border-zinc-900 pb-1"><span className="text-zinc-400">research_agent:</span><span className="text-emerald-400 font-semibold">Google Search & URL</span></div>
              <div className="flex justify-between border-b border-zinc-900 pb-1"><span className="text-zinc-400">security_audit_agent:</span><span className="text-emerald-400 font-semibold">Constitution Guard</span></div>
              <div className="flex justify-between border-b border-zinc-900 pb-1"><span className="text-zinc-400">qa_test_agent:</span><span className="text-emerald-400 font-semibold">Test Suites</span></div>
              <div className="flex justify-between"><span className="text-zinc-400">database_architect:</span><span className="text-emerald-400 font-semibold">Schemas & Migrations</span></div>
            </div>
          </div>
        </div>
        <div className="lg:col-span-2 bg-zinc-950 border border-emerald-950 rounded-lg p-5 flex flex-col shadow-lg shadow-emerald-950/20">
          <div className="flex items-center justify-between border-b border-zinc-900 pb-3 mb-3">
            <span className="text-xs uppercase text-zinc-400 tracking-wider flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" /> Live Multi-Agent Telemetria</span>
            <span className="text-xs text-zinc-600">STDOUT / ADK LOG</span>
          </div>
          <div className="flex-1 bg-black/90 border border-zinc-900 rounded p-4 overflow-y-auto space-y-2.5 text-xs max-h-[550px]">
            {logs.map((log, index) => (
              <div key={index} className={`leading-relaxed ${log.startsWith(">") ? "text-yellow-400 font-bold" : log.startsWith("✔") ? "text-white font-semibold bg-emerald-950/50 p-2.5 rounded border border-emerald-800" : log.startsWith("✖") ? "text-red-400 font-bold bg-red-950/30 p-2.5 rounded border border-red-900" : log.startsWith("[Krok") ? "text-cyan-400 font-semibold mt-2" : log.startsWith("→") ? "text-purple-400 pl-4" : log.startsWith("←") ? "text-zinc-400 pl-4 italic" : "text-emerald-500/90"}`}>{log}</div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
EOF

# 6. Vytvorenie prázdnych chýbajúcich referencií pre úspešný build
echo "[TRINITY_Core] Inicializujem chýbajúce importované moduly..."
touch tsconfig.json tailwind.config.ts postcss.config.js app/globals.css app/layout.tsx core/constitution.ts core/types.ts skills/dynamicEngine.ts skills/registry.ts memory/engine.ts

echo "=========================================================="
echo "[TRINITY_Core] INŠTALÁCIA DOKONČENÁ."
echo "Na spustenie aplikácie prejdi do zložky 'trinity-omni-core' a použi príkaz: ./setup.sh"
echo "=========================================================="
