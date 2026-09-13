// Vetva 3: Delegovanie na Python ADK Backend
      } else {
        try {
          const adkRes = await fetch("http://localhost:8000/api/execute", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt: userGoal })
          });
          
          if (!adkRes.ok) {
            throw new Error(`Python Backend vrátil status: ${adkRes.status}`);
          }
          
          const adkData = await adkRes.json();
          completed = true;
          finalAnswer = adkData.result || `Úloha úspešne vybavená cez TRINITY Core.`;
        } catch (error: any) {
          completed = true;
          finalAnswer = `[CHYBA KOMUNIKÁCIE] Nepodarilo sa spojiť s Python ADK na porte 8000. Skontroluj, či beží agent_engine/main.py. Detail: ${error.message}`;
        }
        currentStep.finalAnswer = finalAnswer;
      }
