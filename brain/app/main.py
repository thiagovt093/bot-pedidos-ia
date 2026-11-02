from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(title="Bot Pedidos IA")


@app.get("/health")
def health() -> dict[str, bool]:
    return {"ok": True}
