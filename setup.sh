#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "   INŠTALÁCIA TRINITY OMNI-CORE (MULTI-AGENT GOOGLE ADK)  "
echo "=========================================================="

# 1. Kontrola prostredia
command -v node >/dev/null 2>&1 || { echo "✖ Node.js nie je nainštalovaný."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "✖ Python3 nie je nainštalovaný."; exit 1; }

echo "✔ Node.js: $(node -v)"
echo "✔ Python3: $(python3 --version)"

# 2. Inštalácia závislostí
echo "📦 Inštalujem Python balíčky (Google ADK, GenAI, Flask)..."
pip install -r requirements.txt

echo "📦 Inštalujem Node.js balíčky (Next.js, Tailwind, Lucide)..."
npm install

echo "🛠️ Pripravujem sandboxing a dátové priečinky..."
mkdir -p generated_apps data memory/data skills/runtime logs

# 3. Paralelný štart služieb
echo "🚀 Spúšťam TRINITY Python Backend (Port 8000)..."
python3 agent_engine/main.py &
PYTHON_PID=$!

# Zabezpečenie automatického vypnutia Python servera pri prerušení skriptu
trap "echo 'Ukončujem TRINITY Python backend...'; kill $PYTHON_PID 2>/dev/null || true" EXIT

echo "🚀 Spúšťam TRINITY Next.js AURA Dashboard (Port 3000)..."
npm run dev
