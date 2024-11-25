from app.cloud.cloud import Cloud
from app.cloud.cloud_client import CloudClient
from app.conf import settings


async def get_cloud_client() -> CloudClient:
    return CloudClient(settings.CLOUD_API_URL, settings.CLOUD_API_TOKEN)


async def get_cloud(client: CloudClient) -> Cloud:
    return Cloud(client, settings.CLOUD_URL)
