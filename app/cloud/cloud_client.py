from typing import Any, Optional, Self
from types import TracebackType
from contextlib import contextmanager
from http import HTTPStatus

import aiohttp

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
        """
        Send an asynchronous GET request to the specified URL.

        Args:
            url (str): The URL.
            params (Optional[dict]): Query parameters.

        Returns:
            dict: The JSON response from the server.
        """

        with self._ensure_ok():
            async with self._connection.get(url, params=params) as response:
                return await response.json()

    async def post(self, url: str, data: Any = None) -> dict:
        """
        Send an POST request to the specified URL.

        Args:
            url (str): The URL.
            data (Any): Data.

        Returns:
            dict: The JSON response from the server.
        """

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
