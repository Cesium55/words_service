from fastapi import FastAPI
from routes import categories_router, debug_init_router, admin_router
from fastapi.middleware.cors import CORSMiddleware
from config import APP_DEBUG


app = FastAPI()

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


@app.get("/")
async def index():
    return {"message": f"Words service index page!"}


