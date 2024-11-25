from typing import BinaryIO

from .cloud_client import CloudClient


class Cloud:
    def __init__(self, client: CloudClient, location: str) -> None:
        self._client = client
        self._location = location

    @property
    def location(self) -> str:
        return self._location

    async def has_folder(self, path: str) -> bool:
        """
        Check if folder with given path exists in cloud storage.

        Args:
            path (str): Path to folder.

        Returns:
            bool: Returns `True` if folder exists.
        """

        response = await self._client.get("has_folder/", {"path": self.get_link(path)})
        return response.get("status") is True

    async def create_file(self, path: str, file: BinaryIO) -> None:
        """
        Create a file in cloud storage.

        Args:
            path (str): Path to file.
            file (BinaryIO): File to upload.
        """

        await self._client.post(f"upload/{self.get_link(path)}", data=file)

    async def delete_file(self, path: str) -> None:
        """
        Delete a file from cloud storage.

        Args:
            path (str): Path to the file to be deleted.
        """

        await self._client.post(f"delete/{self.get_link(path)}")

    def get_link(self, path: str) -> str:
        """
        Generate a full link to a resource in the cloud storage.

        Args:
            path (str): Relative path to the resource.

        Returns:
            str: Full URL to the resource in the cloud storage.
        """

        return f"{self.location}{path}"
