import os
import dlt

from sec_client import fetch_submissions
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


pipeline = dlt.pipeline(
    pipeline_name="filingpulse_sec",
    destination="snowflake",
    dataset_name="RAW",
)


if __name__ == "__main__":
    load_info = pipeline.run(submissions_resource())
    print(load_info)

