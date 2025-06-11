import dlt
from dlt.sources.helpers.rest_client import paginate
from dlt.sources.helpers.rest_client.auth import BearerTokenAuth

from typing import Optional

### Not working, possibly a secret error, but I don't know how to fix it
# https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api?apiVersion=2022-11-28

BASE_GITHUB_URL = "https://api.github.com/repos/{repo_name}"


def fetch_github_data_with_token_and_params(
        repo_name, 
        endpoint, 
        params={}, 
        access_token=None):
    """Fetch data from the GitHub API based on repo_name, endpoint, and params."""
    url = BASE_GITHUB_URL.format(repo_name=repo_name) + f"/{endpoint}"
    return paginate(
        url,
        params=params,
        auth=BearerTokenAuth(token=access_token) if access_token else None,
    )


@dlt.source
def github_source_with_token_and_repo(
    repo_name: str = dlt.config.value,
    access_token: Optional[str] = dlt.secrets.value,
):
    for endpoint in ["issues", "comments", "traffic/clones"]:
        params = {"per_page": 100}
        yield dlt.resource(
            fetch_github_data_with_token_and_params(repo_name, endpoint, params, access_token),
            name=endpoint,
            write_disposition="merge",
            primary_key="id",
        )


pipeline = dlt.pipeline(
    pipeline_name="github_with_source_secrets",
    destination="duckdb",
    dataset_name="github_data",
)
load_info = pipeline.run(github_source_with_token_and_repo())