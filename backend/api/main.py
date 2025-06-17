from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

elo_standings = []
elo_history_map = {}


@app.get("/elo_standings")
async def get_elo_standings():
    """Return current ELO standings for all drivers."""
    return {"standings": elo_standings}


@app.get("/elo/{driver_id}")
async def get_driver_elo(driver_id: str):
    """Return ELO rating history for the given driver."""
    history = elo_history_map.get(driver_id, [])
    return {"driver_id": driver_id, "history": history}
