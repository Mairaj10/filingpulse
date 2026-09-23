import hashlib
import os

import dlt

from sec_client import fetch_submissions, fetch_companyfacts
from s3_storage import upload_bytes


@dlt.resource(
    name="submissions",
    primary_key="accessionNumber",
    write_disposition="merge",
)
def submissions_resource():
    data, raw_bytes, run_timestamp = fetch_submissions()

    bucket_name = os.environ["FILINGPULSE_RAW_BUCKET"]
    object_key = f"apple/{run_timestamp}/submissions.json"

    upload_bytes(
        bucket_name=bucket_name,
        object_key=object_key,
        body=raw_bytes,
    )

    recent = data["filings"]["recent"]
    filing_count = len(recent["accessionNumber"])

    for i in range(filing_count):
        filing = {}

        for key, values in recent.items():
            filing[key] = values[i]

        filing["cik"] = data["cik"]
        filing["company_name"] = data["name"]

        yield filing


@dlt.resource(
    name="company_facts",
    primary_key="observation_id",
    write_disposition="merge",
)
def companyfacts_rows():
    data, raw_bytes, run_timestamp = fetch_companyfacts()

    bucket_name = os.environ["FILINGPULSE_RAW_BUCKET"]
    object_key = f"apple/{run_timestamp}/companyfacts.json"

    upload_bytes(
        bucket_name=bucket_name,
        object_key=object_key,
        body=raw_bytes,
    )

    for taxonomy, concepts in data["facts"].items():
        for concept_name, concept_data in concepts.items():
            for unit, observations in concept_data["units"].items():
                for observation in observations:
                    row = observation.copy()

                    identity = "|".join([
                        str(data["cik"]),
                        taxonomy,
                        concept_name,
                        unit,
                        observation["accn"],
                        observation.get("start", ""),
                        observation.get("end", ""),
                    ])

                    row["observation_id"] = hashlib.sha256(
                        identity.encode()
                    ).hexdigest()

                    row["cik"] = data["cik"]
                    row["company_name"] = data["entityName"]
                    row["taxonomy"] = taxonomy
                    row["concept"] = concept_name
                    row["label"] = concept_data["label"]
                    row["description"] = concept_data["description"]
                    row["unit"] = unit

                    yield row


pipeline = dlt.pipeline(
    pipeline_name="filingpulse_sec",
    destination="snowflake",
    dataset_name="RAW",
)

if __name__ == "__main__":
    load_info = pipeline.run([
        submissions_resource(),
        companyfacts_rows(),
    ])

    print(load_info)