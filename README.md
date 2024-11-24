# file-manager
Simple FastAPI app for files management

## Project structure

```
file-manager
├── app
│   ├── api               # Contains configuration of the app
│   │   ├── dependencies  # FastAPI deps
│   │   └── routers       # All api-routers
│   ├── cloud             # PoC for cloud storage
│   ├── conf              # Contains configuration of the app
│   ├── db
│   │   └── base.py       # Database-related stuff
|   ├── migrations        # Alembic migrations
│   ├── models            # Contains all models
│   │   └── mixins        # Model mixins
│   ├── repositories      # Contains repositories for objects manipulation
│   ├── schemas           # Pydantic schemas
│   ├── services          # Services layer
│   ├── storage           # Different storages impl
│   ├── uow               # UoW impl
│   ├── main.py           # FastAPI Entrypoint
│   └── utils.py          # Some utilities
└── tests                 # Tests for the app
```

## Local development

1. Configure `.env`.

```shell
/file-manager$ > cp example.env .env
```

2. Create virtual environment & install dependencies using `pipenv`.

```shell
/file-manager$ > pipenv install --dev
```

3. Run required docker-containers.

```shell
/file-manager$ > docker compose up -d
```

4. (Optional) Create pre-commit hook for linter (or trigger it manually via `ruff check --fix` and `ruff format`)

```shell
/file-manager$ > pre-commit install
```

5. Apply database migrations.

```shell
/file-manager$> alembic upgrade head
```

6. Start the FastAPI app.

```shell
/file-manager$> cd app/
/file-manager/app$> fastapi dev main.py
```

## Useful links

- http://127.0.0.1:8000/docs - Swagger UI
- http://127.0.0.1:8000/redoc - ReDoc


## Testing streaming

You can send very big files using Request Streaming technique.

Example of this using `requests` and `requests_toolbelt` libraries:

```python
import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

current_dir = os.path.dirname(__file__)

m = MultipartEncoder(
    fields={
        "file": (
            "filename.mp4",
            open("path/to/filename.mp4"), "rb"),
            "video/mp4",
        )
    }
)
r = requests.post(
    "http://127.0.0.1:8000/files/upload",
    data=m,
    headers={"Content-Type": m.content_type},
)
print(r.json())
```
