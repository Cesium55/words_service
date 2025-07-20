from fastapi import FastAPI
from routes import (
    categories_router,
    debug_init_router,
    admin_router,
    words_router,
    langs_router,
)
from fastapi.middleware.cors import CORSMiddleware
from config import APP_DEBUG
from contextlib import asynccontextmanager
from brokers.broker import broker as rabbit_broker


@asynccontextmanager
async def lifespan(app: FastAPI):

    await rabbit_broker.safe_start()

    print("APP STARTED")

    yield

    await rabbit_broker.stop()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if APP_DEBUG:
    app.include_router(debug_init_router)


app.include_router(categories_router)
app.include_router(admin_router)
app.include_router(words_router)
app.include_router(langs_router)


@app.get("/")
async def index():
    return {"message": f"Words service index page!"}
