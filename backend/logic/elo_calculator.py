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


if __name__ == "__main__":
    races = fetch_races(2025, 2025)
    print(f"Fetched {len(races)} total races")
