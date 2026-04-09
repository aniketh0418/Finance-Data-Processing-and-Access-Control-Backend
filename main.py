from fastapi import FastAPI
from contextlib import asynccontextmanager
from config.database import connect_to_mongo, close_mongo_connection
from routes import auth_routes, user_routes, record_routes, dashboard_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title="Finance Analytics API",
    description="Backend API for Finance Data Processing and Access Control",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(record_routes.router)
app.include_router(dashboard_routes.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Finance Analytics API"}
