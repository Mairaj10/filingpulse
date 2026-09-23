import requests
from pathlib import Path
from datetime import datetime, timezone

SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK0000320193.json"

COMPANYFACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json"


HEADERS = {
    "User-Agent": "FilingPulse/1.0 rashdimairaj9@gmail.com"
}

def fetch_submissions():
    response = requests.get(SUBMISSIONS_URL, headers=HEADERS, timeout=30)
    response.raise_for_status()

    run_time = datetime.now(timezone.utc)
    run_timestamp = run_time.strftime("%Y-%m-%dT%H-%M-%SZ")

    output_path = (
        Path("data/raw/apple")
        / run_timestamp
        / "submissions.json"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(response.content)

    data = response.json()

    print(f"Saved raw SEC submissions data to {output_path}")

    return data, response.content, run_timestamp

def fetch_companyfacts():
    response = requests.get(COMPANYFACTS_URL, headers=HEADERS, timeout=30)
    response.raise_for_status()

    run_time = datetime.now(timezone.utc)
    run_timestamp = run_time.strftime("%Y-%m-%dT%H-%M-%SZ")

    output_path = (
        Path("data/raw/apple")
        / run_timestamp
        / "companyfacts.json"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(response.content)

    data = response.json()

    print(f"Saved raw SEC company facts data to {output_path}")

    return data, response.content, run_timestamp

if __name__ == "__main__":
    data, raw_bytes, run_timestamp = fetch_submissions()
    print(data["name"])

