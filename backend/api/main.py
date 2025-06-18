from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.logic.elo_calculator import fetch_races, compute_elo_ratings

app = FastAPI()

races_data = fetch_races(2020, 2025)
elo_standings, elo_history_map = compute_elo_ratings(races_data)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/elo_standings")
async def get_elo_standings():
    """Return current ELO standings for all drivers."""
    return {"standings": elo_standings}


@app.get("/elo/{driver_id}")
async def get_driver_elo(driver_id: str):
    """Return ELO rating history for the given driver."""
    history = elo_history_map.get(driver_id, [])
    return {"driver_id": driver_id, "history": history}
