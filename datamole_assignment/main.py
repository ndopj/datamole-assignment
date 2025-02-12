from typing import Union

import uvicorn
from fastapi import FastAPI

from datamole_assignment.setup import config
from datamole_assignment.service import GithubEventsService


app = FastAPI()
github = GithubEventsService()


@app.get("/")
async def read_root():
    response = await github.events("fastapi", "fastapi")
    return response


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == '__main__':
    uvicorn.run("datamole_assignment.main:app",
                port=config.port,
                log_level=config.log_level.lower(),
                reload=config.hot_reload,
                log_config=config.log_config)
