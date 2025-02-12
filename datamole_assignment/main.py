from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from datamole_assignment.setup import config, services
from datamole_assignment.service import GithubEventsService


@asynccontextmanager
async def lifespan(app: FastAPI):
    github = GithubEventsService()
    services["github_events"] = github
    yield # Application runtime. Start -> yield -> Stop
    await github.close()
    services.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    github: GithubEventsService = services["github_events"]
    response = await github.events("fastapi", "fastapi")
    return response


if __name__ == '__main__':
    uvicorn.run("datamole_assignment.main:app",
                port=config.port,
                log_level=config.log_level.lower(),
                reload=config.hot_reload,
                log_config=config.log_config)
