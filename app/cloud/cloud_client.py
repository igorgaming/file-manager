from contextlib import contextmanager
from typing import Any, Optional, Self
from types import TracebackType
from http import HTTPStatus
import aiohttp

from app.conf import settings
from .exceptions import InternalError, InvalidApiKey, NotFound, ClientError


class CloudClient:
    def __init__(self, api_url: str, api_token: str) -> None:
        self._api_url = api_url
        self._api_token = api_token

        self._start_connection()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self._close_connection()

    async def get(self, url: str, params: Optional[dict] = None) -> dict:
        with self._ensure_ok():
            async with self._connection.get(url, params=params) as response:
                return await response.json()

    async def post(self, url: str, data: Any = None) -> dict:
        with self._ensure_ok():
            async with self._connection.post(url, data=data) as response:
                return await response.json()

    @contextmanager
    def _ensure_ok(self):
        try:
            yield
        except aiohttp.ClientResponseError as e:
            if e.status == HTTPStatus.UNAUTHORIZED:
                raise InvalidApiKey from e
            elif e.status == HTTPStatus.NOT_FOUND:
                raise NotFound from e
            else:
                raise InternalError from e
        except aiohttp.ClientError as e:
            raise ClientError from e

    def _start_connection(self) -> None:
        with self._ensure_ok():
            self._connection: aiohttp.ClientSession = aiohttp.ClientSession(
                base_url=self._api_url,
                headers={"Authorization": f"Bearer {self._api_token}"},
            )

    async def _close_connection(self) -> None:
        await self._connection.close()


async def get_cloud_client() -> CloudClient:
    return CloudClient(settings.CLOUD_API_URL, settings.CLOUD_API_TOKEN)
