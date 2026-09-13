import { NextResponse } from "next/server";
import { TrinityOrchestrator } from "../../../core/orchestrator";

// Inicializácia orchestrátora
const orchestrator = new TrinityOrchestrator();

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { prompt } = body;

    if (!prompt) {
      return NextResponse.json({ status: "ERROR", error: "Príkaz je prázdny." }, { status: 400 });
    }

    // Spustenie autonómnej slučky
    const result = await orchestrator.executeTask(prompt);

    if (result.success) {
      return NextResponse.json({ status: "SUCCESS", data: result });
    } else {
      return NextResponse.json({ status: "ERROR", error: result.finalAnswer }, { status: 403 });
    }

  } catch (error: any) {
    return NextResponse.json({ status: "ERROR", error: error.message }, { status: 500 });
  }
}
