from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings


app = FastAPI(title='File manager app.', version='0.1.0')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)