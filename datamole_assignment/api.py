import statistics
from datetime import timedelta

from fastapi import APIRouter
from starlette.responses import RedirectResponse

from datamole_assignment.setup import services
from datamole_assignment.service import GithubService, Event, EventType


events_router = APIRouter()
root_router = APIRouter()


@root_router.get("/", status_code=307, include_in_schema=False)
async def get_root() -> RedirectResponse:
    # Redirect root GET requests to the API docs
    return RedirectResponse(url="swagger-ui.html")


@events_router.get("/{owner}/{repo}/mean")
async def events_mean(owner: str, repo: str, type: EventType = None) -> timedelta:
    github: GithubService = services["github"]
    previous_time = None
    time_diffs = []

    async for event in github.events(owner, repo):
        if type is None or event.type == type:
            if previous_time is None:
                previous_time = event.created_at
            time_diff = event.created_at - previous_time
            time_diffs.append(time_diff.seconds)

    if len(time_diffs) == 0:
        return timedelta(seconds=0)
    return timedelta(seconds=statistics.fmean(time_diffs))
