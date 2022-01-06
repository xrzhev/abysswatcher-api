from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from concurrent import futures

from routers import certs, notice


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(certs.router)
app.include_router(notice.router)
