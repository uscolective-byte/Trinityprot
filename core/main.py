import os
import json
from flask import Flask, request, jsonify
from agents import root_agent

app = Flask(__name__)

@app.route("/api/health", methods=["GET"])
def health():
    """
    Diagnostický endpoint pre overenie stavu jadra a zoznamu aktívnych sub-agentov.
    """
    return jsonify({
        "status": "ONLINE",
        "system": "TRINITY_Core Multi-Agent ADK",
        "sub_agents": [
            "app_builder_agent",
            "devops_deploy_agent",
            "research_agent",
            "security_audit_agent",
            "qa_test_agent",
            "database_architect"
        ]
    })

@app.route("/api/execute", methods=["POST"])
def execute_plan():
    """
    Hlavný exekučný endpoint. Prijíma príkazy z AURA Dashboardu a deleguje ich
    na centrálneho orchestrátora (TRINITY Core).
    """
    data = request.get_json() or {}
    prompt = data.get("prompt")
    
    if not prompt:
        return jsonify({"error": "Prompt je povinný"}), 400

    # Delegovanie spracovania cez TRINITY Core root agenta
    try:
        response = root_agent.run(prompt)
        return jsonify({
            "status": "SUCCESS",
            "orchestrator": "TRINITY_Core",
            "result": str(response)
        })
    except Exception as e:
        return jsonify({
            "status": "ERROR", 
            "message": str(e)
        }), 500

if __name__ == "__main__":
    # Spustenie TRINITY backendu na porte 8000
    app.run(host="0.0.0.0", port=8000, debug=False)
