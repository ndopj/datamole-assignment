from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from datamole_assignment.setup import config, services
from datamole_assignment.service import GithubService
from datamole_assignment.api import events_router, root_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    github = GithubService()
    services["github"] = github
    yield # Application runtime. Start -> yield -> Stop
    await github.close()
    services.clear()


app = FastAPI(lifespan=lifespan, docs_url="/swagger-ui.html")
app.include_router(root_router)
app.include_router(events_router, prefix="/v1/events", tags=["Events API"])


if __name__ == '__main__':
    uvicorn.run("datamole_assignment.main:app",
                host=config.host,
                port=config.port,
                log_level=config.log_level.lower(),
                reload=config.hot_reload,
                log_config=config.log_config)
