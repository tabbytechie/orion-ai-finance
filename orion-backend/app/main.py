from fastapi import FastAPI
from app.core.database import engine, Base
from app.modules.auth import routes as auth_routes
from app.modules.transactions import routes as transaction_routes
from app.modules.ai import routes as ai_routes
from app.modules.analytics import routes as analytics_routes

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Orion - AI-Powered Financial Control Hub",
    description="The backend for the Orion financial control hub.",
    version="0.1.0",
)

# Include module routers
app.include_router(auth_routes.router, prefix="/api/v1")
app.include_router(transaction_routes.router, prefix="/api/v1")
app.include_router(ai_routes.router, prefix="/api/v1")
app.include_router(analytics_routes.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Orion Backend"}