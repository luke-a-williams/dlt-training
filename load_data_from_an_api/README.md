# Overview
This section continues the initial tutorial in [load-data-from-an-api](https://dlthub.com/docs/tutorial/load-data-from-an-api#create-a-pipeline) but also goes into the referenced tutorial [rest-api](https://dlthub.com/docs/tutorial/rest-api) **first** for more detail and learning.

## What is a REST API?
A REST API (REpresentational State Transfer Application Programming Interface) is a standard way for applications to communicate with each other over the internet. It uses HTTP methods (GET, POST, PUT, DELETE, etc.) to perform actions on data, typically in formats like JSON or XML. REST APIs are stateless, meaning each request contains all the necessary information, and the server doesn't store any context between requests. 

### Configuration
Let's break down the configuration of the REST API source. It consists of three main parts: `client`, `resource_defaults`, and `resources`.
```
config: RESTAPIConfig = {
    "client": {
        # ...
    },
    "resource_defaults": {
        # ...
    },
    "resources": [
        # ...
    ],
}
```

## Pokemon example
I had an issue running the tutorial here as I was affected by a rate limit that wasn't in the tutorial.
I commented out the github api tutorial and aim to look at that one in the original tutorial, but for now want to follow the pokemon tutorial. This worked temporarily for the pokemon case.

## Github issues example
I've had to blend the tutorials a bit because the github_issues.py script provided is too simplistic and doesn't let you use secrets by default until later in the tutorial, and without that api key you can get rate limited. 

### How to get the more complex github example working
You need to use a [fine-grained personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)
Set this `access_token` in your secrets.toml file. I couldn't find a tutorial for this on DLT but you can look at the `rest_api_pipeline.py` to see the github source has been defined to take an access_key from the secrets file by default

### Write disposition
- [Replacing the data](https://dlthub.com/docs/tutorial/)rest-api#replacing-the-data
- [Merging the data](https://dlthub.com/docs/tutorial/rest-api#merging-the-data)
You can set this in the resource_defaults, and a replace definition is clever enough to know to replace existing rows with the new data, avoiding duplicates. It even works if you didn't set this first time, have duplicates, and run it again. It removes them all.

- [Loading the data incrementally](https://dlthub.com/docs/tutorial/rest-api#loading-data-incrementally)
APIs that support incremental loading usually provide a way to fetch only new or changed data (most often by using a timestamp field like updated_at, created_at, or incremental IDs).

## Tips
Between pipeline runs, dlt keeps the state in the same database it loaded data into. Peek into that state, the tables loaded, and get other information with:

`dlt pipeline -v github_issues_incremental info`
or
`uv run dlt pipeline -v github_issues_incremental info`

You can also view the last trace with

`dlt pipeline github_issues_incremental trace`
or 
`uv run dlt pipeline github_issues_incremental trace`

You can find more information on inspecting a pipeline after loading:
[Inspect a Load Process](https://dlthub.com/docs/walkthroughs/run-a-pipeline#4-inspect-a-load-process)
