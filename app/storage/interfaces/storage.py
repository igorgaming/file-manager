from typing import Protocol

from fastapi import UploadFile


class IStorage(Protocol):
    @property
    def location(self) -> str:
        """Get the base directory.

        Returns:
            str: Path to the base directory.
        """

    def get_absolute_path(self, path: str) -> str:
        """Get absolute path.

        Args:
            path (str): Path to file.

        Returns:
            str: Returns absolute path to the file.
        """

    async def exists(self, path: str) -> bool:
        """Check if file with given path exists.

        Args:
            path (str): Path to file.

        Returns:
            bool: Returns `True` if file exists.
        """

    async def save(self, file: UploadFile, save_to: str) -> str:
        """Save `UploadedFile` to storage.

        Args:
            file (UploadFile): Uploaded file.
            save_to (str): Path to save the file.

        Returns:
            str: Path to file.
        """

    async def delete(self, path: str) -> None:
        """Delete file from storage.

        Args:
            path (str): Path to file.
        """
