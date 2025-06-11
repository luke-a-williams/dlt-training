import dlt
from dlt.sources.helpers import requests
from typing import Any, Iterable

@dlt.resource(
        table_name="issues", 
        write_disposition="merge",
        primary_key="id",
)
def get_issues(
    updated_at=dlt.sources.incremental("updated_at", initial_value="1970-01-01T00:00:00Z")
) -> Iterable[Any]:
    """
    Fetches issues from the GitHub API.
    # NOTE: we read only open issues to minimize number of calls to the API.
    # There's a limit of ~50 calls for not authenticated Github users.
    """

    # Pay attention to how we use the since parameter from the GitHub API and updated_at.last_value 
    # to tell GitHub to return issues updated only after the date we pass. 
    # updated_at.last_value holds the last updated_at value from the previous run.
    url = (
        "https://api.github.com/repos/dlt-hub/dlt/issues"
        f"?since={updated_at.last_value}&per_page=100&sort=updated"
        "&directions=desc&state=open"
    )

    while True:
        # Make a request to the GitHub API
        response = requests.get(url)
        response.raise_for_status()
        yield response.json()

        # Stop requesting pages if the last element was already
        # older than initial value
        # Note: incremental will skip those items anyway, we just
        # do not want to use the api limits

        # get next page
        if "next" not in response.links:
            break
        url = response.links["next"]["url"]

pipeline = dlt.pipeline(
    pipeline_name="github_issues_merge",
    destination="duckdb",
    dataset_name="github_data_merge",
)
# The response contains a list of issues
load_info = pipeline.run(get_issues)
row_counts = pipeline.last_trace.last_normalize_info

print(row_counts)
print("------")
print(load_info)