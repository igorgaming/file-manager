from io import BytesIO

import pytest
from unittest.mock import AsyncMock
from httpx import AsyncClient
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import File
from tests.fixtures import FakeStorage


@pytest.mark.asyncio
async def test_upload(
    client: AsyncClient,
    db: AsyncSession,
    fake_storage: FakeStorage,
    fake_cloud_client: AsyncMock,
):
    response = await client.post(
        "/files/upload",
        files={
            "file": ("test.txt", BytesIO(b"test"), "text/plain"),
        },
    )
    data = response.json()

    assert response.status_code == 201
    assert len(fake_storage.items) == 1
    assert fake_cloud_client.is_called is True

    res = await db.scalar(
        select(
            exists(File).where(
                File.uuid == data["uuid"],
                File.original_name == "test.txt",
                File.content_type == "text/plain",
                File.path == list(fake_storage.items.keys())[0],
            )
        )
    )
    assert res is True


@pytest.mark.asyncio
async def test_upload_without_file(
    client: AsyncClient,
):
    response = await client.post(
        "/files/upload",
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_download(
    client: AsyncClient,
    fake_file: File,
):
    response = await client.get(
        f"/files/download/{fake_file.uuid}",
    )

    assert response.status_code == 200
    assert response.headers.get("Content-Type") == "application/octet-stream"
    assert (
        response.headers.get("Content-Disposition")
        == f'attachment; filename="{fake_file.original_name}"'
    )


@pytest.mark.asyncio
async def test_download_unexisting_uuid(
    client: AsyncClient,
):
    response = await client.get(
        "/files/download/70ef006f-ebcd-49e3-bb0e-79ca5c31f062",
    )
    assert response.status_code == 404
