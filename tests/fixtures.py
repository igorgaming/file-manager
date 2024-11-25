import os
from typing import Any
import unittest.mock

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, UploadFile
import pytest_asyncio

from app.models import File
from app.dependencies import IStorage, get_filesystem_storage
from app.conf import settings


class FakeStorage(IStorage):
    def __init__(self) -> None:
        self.items: dict[str, Any] = {}

    @property
    def location(self) -> str:
        return os.path.join(os.path.abspath(settings.APP_BASE_DIR), "..", "tests")

    def get_absolute_path(self, path: str) -> str:
        return os.path.join(self.location, path)

    async def exists(self, path: str) -> bool:
        return path in self.items

    async def save(self, file: UploadFile, save_to: str) -> str:
        self.items[save_to] = file
        return save_to

    async def delete(self, path: str) -> None:
        self.items.pop(path, None)


class FakeCloudClient:
    def __init__(self, *args, **kwargs):
        self.is_called = False

    async def post(self, *args, **kwargs):
        self.is_called = True

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass


@pytest_asyncio.fixture
async def fake_storage(app: FastAPI):
    storage = FakeStorage()
    app.dependency_overrides[get_filesystem_storage] = lambda: storage
    return storage


@pytest_asyncio.fixture
async def fake_cloud_client():
    client = FakeCloudClient()
    with unittest.mock.patch(
        "app.dependencies.cloud.CloudClient", lambda *args, **kwargs: client
    ):
        yield client


@pytest_asyncio.fixture
async def fake_file(
    db: AsyncSession,
    fake_storage: FakeStorage,
):
    file = File(
        uuid="70ef006f-ebcd-49e3-bb0e-79ca5c31f062",
        path="data/file.txt",
        original_name="test.txt",
        size="",
        content_type="text/plain",
    )
    db.add(file)
    await db.commit()
    db.expunge(file)

    fake_storage.items["data/file.txt"] = b"test"

    return file
