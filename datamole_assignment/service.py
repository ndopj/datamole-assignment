from enum import Enum
from datetime import datetime
from typing import AsyncGenerator, Optional

import httpx
from pydantic import BaseModel, field_validator

from datamole_assignment.setup import config, log


class EventType(str, Enum):
    WATCH_EVENT = 'WatchEvent'
    PULL_REQUEST_EVENT = 'PullRequestEvent'
    ISSUES_EVENT = 'IssuesEvent'

class Event(BaseModel):
    id: int
    created_at: datetime
    type: Optional[EventType] = None

    @field_validator("type", mode="before")
    @classmethod
    def validate_event_type(cls, value):
        # if unexpected value is encountered set None instead of raising an error
        return value if value in EventType.__members__.values() else None


class GithubService:

    def __init__(self):
        # https://docs.github.com/en/rest/activity/events?apiVersion=2022-11-28#list-public-events-for-a-network-of-repositories
        self.client = httpx.AsyncClient(
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": config.github_api_version,
            }
        )
        log.info(f"Initialized async client "
                  f"[base_url: {self.client.base_url}, "
                  f"headers: {self.client.headers}]")


    async def close(self):
        await self.client.aclose()
        log.info("Closed async client")


    async def events(self, owner: str, repo: str) -> AsyncGenerator[Event, None]:
        """**Streams repository events from paginated GitHub Events API via async generator.**  
          
        Crawls throught all of the pages, yielding Events from each response.  
        If generator is stopped, any yet remaining pages will not be fetched.  
          
        *`datamole_assignment.setup.Settings` configures page size during application startup.*  

        Github is using resposne header links for pagination.
        - https://docs.github.com/en/rest/activity/events?apiVersion=2022-11-28#list-public-events-for-a-network-of-repositories
        - https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api?apiVersion=2022-11-28#using-link-headers
        """
        url = f"{config.github_url}/networks/{owner}/{repo}/events"
        params = {"per_page": config.github_page_size, "page": 1}
        url = self.client.build_request("GET", url, params=params).url

        while url:
            response = await self.client.get(url)
            response.raise_for_status()
            url = None if "next" not in response.links else response.links["next"]["url"]
            for raw_event in response.json():
                yield Event.model_validate(raw_event)
