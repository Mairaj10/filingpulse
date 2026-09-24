import requests
from pathlib import Path
from datetime import datetime, timezone

SUBMISSIONS_URL = "https://data.sec.gov/submissions"

COMPANYFACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts"


HEADERS = {
    "User-Agent": "FilingPulse/1.0 rashdimairaj9@gmail.com"
}

def fetch_submissions(cik):
    padded_cik = str(cik).zfill(10)

    url = f"{SUBMISSIONS_URL}/CIK{padded_cik}.json"

    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()

    run_time = datetime.now(timezone.utc)
    run_timestamp = run_time.strftime("%Y-%m-%dT%H-%M-%SZ")

    output_path = (
        Path("data/raw")
        / padded_cik
        / run_timestamp
        / "submissions.json"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(response.content)

    data = response.json()

    print(f"Saved raw SEC submissions data to {output_path}")

    return data, response.content, run_timestamp

def fetch_companyfacts(cik):
    padded_cik = str(cik).zfill(10)

    url = f"{COMPANYFACTS_URL}/CIK{padded_cik}.json"

    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()

    run_time = datetime.now(timezone.utc)
    run_timestamp = run_time.strftime("%Y-%m-%dT%H-%M-%SZ")

    output_path = (
        Path("data/raw")
        / padded_cik
        / run_timestamp
        / "companyfacts.json"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(response.content)

    data = response.json()

    print(f"Saved raw SEC company facts data to {output_path}")

    return data, response.content, run_timestamp

if __name__ == "__main__":
    data, raw_bytes, run_timestamp = fetch_submissions(320193)
    print(data["name"])

