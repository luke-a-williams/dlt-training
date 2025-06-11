import dlt
from dlt.sources.helpers.rest_client import paginate
from dlt.sources.helpers.rest_client.auth import BearerTokenAuth

from typing import Optional

### Not working, possibly a secret error, but I don't know how to fix it
# https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api?apiVersion=2022-11-28

BASE_GITHUB_URL = "https://api.github.com/repos/dlt-hub/dlt"

def fetch_github_data_with_token(endpoint, params={}, access_token=None):
    url = f"{BASE_GITHUB_URL}/{endpoint}"
    return paginate(
        url,
        params=params,
        auth=BearerTokenAuth(token=access_token) if access_token else None,
    )

@dlt.source
def github_source_with_token(access_token: Optional[str] = dlt.secrets.value):
    for endpoint in ["issues", "comments", "traffic/clones"]:
        params = {"per_page": 100}
        # I could not figure out how to do the seperate params, kept getting an error
        # You can do this simplifying for incremental loading but I don't understand how
        yield dlt.resource(
            fetch_github_data_with_token(endpoint, params, access_token),
            name=endpoint,
            write_disposition="merge",
            primary_key="id",
        )

pipeline = dlt.pipeline(
    pipeline_name='github_dynamic_source',
    destination='duckdb',
    dataset_name='github_data',
)
load_info = pipeline.run(github_source_with_token())
row_counts = pipeline.last_trace.last_normalize_info