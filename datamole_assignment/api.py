import io
import statistics
from datetime import datetime, timezone, timedelta
from typing import AsyncGenerator

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from starlette.responses import RedirectResponse

from datamole_assignment.setup import services, log
from datamole_assignment.service import Event, GithubService, EventType


events_router = APIRouter()
root_router = APIRouter()


@root_router.get("/", status_code=307, include_in_schema=False)
async def get_root() -> RedirectResponse:
    # Redirect root GET requests to the API docs
    return RedirectResponse(url="swagger-ui.html")


@events_router.get("/{owner}/{repo}/mean_time")
async def events_mean_time(owner: str, repo: str, type: EventType = None) -> timedelta:
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


@events_router.get("/{owner}/{repo}/grouped")
async def events_grouped(
    owner: str, repo: str,
    offset: int = Query(None, description="Max time offset in minutes")
) -> dict[EventType, int]:
    github: GithubService = services["github"]
    groups = await group_events(github.events(owner, repo), offset)
    return groups


@events_router.get("/{owner}/{repo}/grouped/graph", response_class=StreamingResponse)
async def events_grouped_graph(
    owner: str, repo: str,
    offset: int = Query(None, description="Max time offset in minutes")
) -> dict[EventType, int]:
    github: GithubService = services["github"]
    groups = await group_events(github.events(owner, repo), offset)
    buf = barplot(groups)
    return StreamingResponse(
        buf, media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=barplot.png"}
    )


async def group_events(events: AsyncGenerator[Event, None], offset: int | None) -> dict[EventType, int]:
    groups = {}
    now = datetime.now(timezone.utc)
    async for event in events:
        if offset is not None and event.created_at < (now - timedelta(minutes=offset)):
            return groups
        if event.type is not None:
            groups[event.type] = groups.get(event.type, 0) + 1
    return groups


def barplot(groups: dict[EventType, int]) -> io.BytesIO:
    """Create a barplot from grouped events.  
    Each event type is represented by a different color.  

    :returns: BytesIO buffer with binary data of the generated .png graph
    """
    labels = list(groups.keys())
    counts = list(groups.values())
    colors = plt.cm.get_cmap("tab10", len(labels)).colors
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(labels, counts, color=colors)
    ax.set_title("Github events grouped by expected types")
    ax.set_xlabel("Type")
    ax.set_ylabel("Count")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return buf
