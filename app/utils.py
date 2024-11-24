from typing import Optional
from datetime import datetime
import hashlib
import os
import random
import string


def get_random_string(
    length: int, characters=string.ascii_letters + string.digits
) -> str:
    """Generate a random string from a given length using the given characters."""

    return "".join(random.choice(characters) for _ in range(length))


class UploadTo:
    """Generates the upload file path with prefix relative to the year and month so that many files do not accumulate at the same level."""

    def __init__(self, prefix: str = "") -> None:
        """
        Args:
            prefix (str): Prefix for upload path.
        """

        self.prefix = prefix

    def __call__(self, filename: Optional[str] = None) -> str:
        today = datetime.now().today()

        parts: list[str] = []
        if self.prefix:
            parts.append(self.prefix)

        parts.extend(
            [
                str(today.year),
                str(today.month),
            ]
        )

        hash = hashlib.sha1(
            get_random_string(12).encode(), usedforsecurity=False
        ).hexdigest()[:32]

        if filename is not None:
            _, ext = os.path.splitext(filename)
        else:
            ext = ""

        parts.append(f"{hash}{ext}")

        return "/".join(parts)
