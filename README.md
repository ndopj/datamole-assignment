<h1 align="center">Datamole Assignment - Norbert Dopjera</h1>

## Table Of Contents

- [About the Project](#about-the-project)
- [Requirements](#requirements)
- [Local development](#local-development)
- [Docker](#docker)
- [Usage](#usage)


## About The Project

*The aim of this assignment is to monitor activities happening on GitHub. For that we want you to stream specific events from the Github API (https://api.github.com/events). The events we are interested in are the WatchEvent, PullRequestEvent and IssuesEvent. Based on the collected events, metrics shall be provided at any time via a REST API to the end user. The following metrics should be implemented:  - Calculate the average time between pull requests for a given repository.  - Return the total number of events grouped by the event type for a given    offset. The offset determines how much time we want to look back i.e., an offset of 10 means we count only the events which have been created in the last 10 minutes.*

> **Bonus assignment** - Add another REST API endpoint providing a meaningful visualization of one of existing metrics or a newly introduced metric

## Requirements
- [Python >= 3.10](https://www.python.org/downloads/release/python-381/)
- [Poetry >= 2.0](https://github.com/python-poetry/poetry)
- [Docker >= 27.0.1](https://www.python.org/downloads/release/python-381/) *(optional - altough older may work as well)*

## Local development

### Poetry
This project is using [Poetry](https://github.com/python-poetry/poetry) and it is recommended to setup dedicated virtual environment for it.  

[https://python-poetry.org/docs/#installing-manually](https://python-poetry.org/docs/#installing-manually)
```shell
# activate your virtualenv with preferred tool before running bellow commands
# e.g. python3 -m venv $VENV_PATH

pip install -U pip setuptools
pip install poetry
```

### Dependencies
> You might want to try removing `poetry.lock` file in case of issues.
```shell
poetry install
```

### Run + Configuration
> All of the configuration options are located at `datamole_assignment.setup.Settings` class.  
Each option can be overridden by exporting ENV variable.  

```shell
# hot-reloading will allow you to dynamically change code while the application is running
export HOT_RELOAD=True
export LOG_LEVEL=DEBUG
poetry run python -m datamole_assignment.main
```

## Docker

In case you don't want to fight with python environments locally you can also use Dockerfile dedicated for this project development.

```shell
docker build -t datamole-assignment .
```

> Additionaly you might want to map a volume while starting the container. Built image will support hot-reloading, so you can make changes to the code dynamically while the image is running.  

```shell
docker run -it -d -p 8080:8080 -v ./datamole_assignment/:/app/datamole_assignment/ datamole-assignment:latest
```

## Usage

Assignment implementation exposes two HTTP endpoints.  
> replace `{owner}` and `{repo}` in bellow paths with identifiers for existing public Github repository.  

```shell
curl -X 'GET' \
  'http://localhost:8080/v1/events/fastapi/fastapi/mean_time?type=PullRequestEvent' \
  -H 'accept: application/json'
```
```shell
curl -X 'GET' \
  'http://localhost:8080/v1/{owner}/{repo}/fastapi/grouped?offset=3000' \
  -H 'accept: application/json'
```  

**You can also navigate to**
- `http://localhost:8080/`  
- `http://localhost:8080/swagger-ui.html`  

**to explore all available options or to communicate with API easily via Swagger Web UI docs for this application.**  

> in some cases I've noticed some repositories reporting events with long delays. Keep this in mind while evaluating grouping endpoint and using offest.

### Github quota limits
By default, the application does not authenticate with Github since it was not requested in the assignment. If you happen to run out of quota limit for your IP, you can temporarily add auth header to the Github client with your *(classic)* [personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

> in file `datamole_assignment/service.py` replace headers in class `GithubService` with following:  
```python
    self.client = httpx.AsyncClient(
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": config.github_api_version,
            "Authorization": "Bearer YOUR-TOKEN"
        }
    )
```