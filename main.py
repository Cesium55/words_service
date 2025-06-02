from fastapi import FastAPI
from routes.debug_init import router as debug_init_router
from routes.categories import router as categories_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if 1:
    app.include_router(debug_init_router)


app.include_router(categories_router)


@app.get("/")
async def index():
    return {"message": f"Words service index page!"}


