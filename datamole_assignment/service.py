import httpx

from datamole_assignment.setup import config, log


class GithubEventsService:

    def __init__(self):
        # https://docs.github.com/en/rest/activity/events?apiVersion=2022-11-28#list-public-events-for-a-network-of-repositories
        self.client = httpx.AsyncClient(
            base_url=config.github_url,
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            }
        )
        log.info(f"Initialized async client "
                  f"[base_url: {self.client.base_url}, "
                  f"headers: {self.client.headers}]")


    async def close(self):
        await self.client.aclose()
        log.info("Closed async client")


    async def events(self, owner: str, repo: str) -> dict[str, any]:
        response = await self.client.get(f"/networks/{owner}/{repo}/events")
        return response.json()
