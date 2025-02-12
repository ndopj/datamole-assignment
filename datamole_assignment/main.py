from typing import Union

import uvicorn
from fastapi import FastAPI

from datamole_assignment.setup import config, log

app = FastAPI()


@app.get("/")
def read_root():
    log.info(f"Github URL: {config.github_url}")
    log.debug("This is a debug messages")
    log.warning("This is a warning message")
    log.error("This is an error message")
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == '__main__':
    uvicorn.run("datamole_assignment.main:app",
                port=config.port,
                log_level=config.log_level.lower(),
                reload=config.hot_reload,
                log_config=config.log_config)
