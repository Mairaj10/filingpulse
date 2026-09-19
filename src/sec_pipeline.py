import dlt
from sec_client import fetch_submissions

@dlt.resource(name="submissions")
def submissions_resource():
    data = fetch_submissions()
    yield data