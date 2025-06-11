# Overview
Copy any notes from Obsidian here

## Installation
https://dlthub.com/docs/reference/installation
The guide there uses pip rather than a pyproject.toml, which needs to be activated in your terminal with `source .venv/bin/activate`. If I encounter problems with this, I will switch to pyproject.toml

## Learning steps
I intend to follow the following tutorials today:

- [Load data from Pure Python data structures](https://dlthub.com/docs/tutorial/load-data-from-an-api)
- [Load data from a REST API](https://dlthub.com/docs/tutorial/rest-api)
- [Load data from a SQL database](https://dlthub.com/docs/tutorial/sql-database)
- [Load data from a cloud storage or a file system](https://dlthub.com/docs/tutorial/filesystem)

### [Load data from Pure Python data structures](https://dlthub.com/docs/tutorial/load-data-from-an-api)

- Loading data from a list of Python dictionaries into DuckDB.
- Low-level API usage with a built-in HTTP client.
- Understand and manage data loading behaviors.
- Incrementally load new data and deduplicate existing data.
- Dynamic resource creation and reducing code redundancy.
- Group resources into sources.
- Securely handle secrets.
- Make reusable data sources.


### Exploring the data
DLT has streamlit built in, to view a streamlit dashboard of the data for basic exploration, use:
- `source .venv/bin/activate`
- `uv run dlt pipeline quick_start show`