from fastapi import APIRouter
from starlette.responses import RedirectResponse

from datamole_assignment.setup import services
from datamole_assignment.service import GithubService


events_router = APIRouter()
root_router = APIRouter()


@root_router.get("/", status_code=307, include_in_schema=False)
async def get_root() -> RedirectResponse:
    # Redirect root GET requests to the API docs
    return RedirectResponse(url="swagger-ui.html")


@events_router.get("/")
async def events():
    github: GithubService = services["github"]
    response = await github.events("fastapi", "fastapi")
    return response
