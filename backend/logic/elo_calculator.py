import requests

BASE_URL = "https://api.jolpi.ca/ergast/f1"


def fetch_races(start_year: int, end_year: int):
    """Fetch all race results from Jolpica API for all seasons in [start_year, end_year]"""
    all_races = []

    for year in range(start_year, end_year + 1):
        races = []
        limit = 100
        offset = 0

        while True:
            url = f"{BASE_URL}/{year}/results.json?limit={limit}&offset={offset}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                page_races = data["MRData"]["RaceTable"]["Races"]
                if not page_races:
                    break
                races.extend(page_races)
                offset += limit
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data for {year}: {e}")
                break

        print(f"Fetched {len(races)} races for {year}")
        all_races.extend(races)

    return all_races


def compute_elo_ratings(races):
    """Compute ELO ratings for drivers"""
    elo = {}
    history = {}
    K = 20
    base_rating = 1000

    for race in races:
        race_id = f"{race['season']} Round {race['round']}"
        team_results = {}

        # Group results by constructor
        for result in race["Results"]:
            driver_id = result["Driver"]["driverId"]
            constructor = result["Constructor"]["name"]
            position_text = result.get("position")
            status = result.get("status")

            if driver_id not in elo:
                elo[driver_id] = base_rating
                history[driver_id] = []

            try:
                position = int(position_text)
            except:
                position = None

            team_results.setdefault(constructor, []).append(
                (driver_id, position, status)
            )

        # For each constructor in this race, update ELO based on teammate comparison
        for constructor, drivers in team_results.items():
            if len(drivers) != 2:
                continue

            (drvA, posA, statusA), (drvB, posB, statusB) = drivers
            winner, loser = None, None

            if posA is None and posB is None:
                # Both drivers did not finish
                continue
            elif posB is None or (
                posA is not None and posB is not None and posA < posB
            ):
                # drvA finished better than drvB
                winner, loser = drvA, drvB
            elif posA is None or (
                posA is not None and posB is not None and posB < posA
            ):
                # drvB finished better than drvA
                winner, loser = drvB, drvA
            else:
                # Both drivers finished in the same position (somehow)
                continue

            Ra, Rb = elo[winner], elo[loser]
            expected_a = 1 / (1 + 10 ** ((Rb - Ra) / 400))
            expected_b = 1 - expected_a

            elo[winner] = Ra + K * (1 - expected_a)
            elo[loser] = Rb + K * (0 - expected_b)

            history[winner].append({"race": race_id, "elo": round(elo[winner])})
            history[loser].append({"race": race_id, "elo": round(elo[loser])})

    standings = sorted(
        [{"driver": d, "elo": round(r, 2)} for d, r in elo.items()],
        key=lambda x: x["elo"],
        reverse=True,
    )

    return standings, history


if __name__ == "__main__":
    races = fetch_races(2020, 2025)
    print(f"Fetched {len(races)} total races")

    if races:
        standings, history = compute_elo_ratings(races)

        print("\nTop 10 Elo Standings:")
        for rank, entry in enumerate(standings[:10], start=1):
            print(f"{rank}. {entry['driver']}: {entry['elo']}")
    else:
        print("No races found for the specified year(s)")
