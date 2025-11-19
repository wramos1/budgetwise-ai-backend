"""
BudgetWise AI API - Main Application Entry Point
FastAPI application with CORS, routers, and database initialization
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine
from app.models import user, transaction, budget, category, goal, badge
from app.routers import auth, users, transactions, budgets, categories, goals, ai

# Create database tables
user.Base.metadata.create_all(bind=engine)
transaction.Base.metadata.create_all(bind=engine)
budget.Base.metadata.create_all(bind=engine)
category.Base.metadata.create_all(bind=engine)
goal.Base.metadata.create_all(bind=engine)
badge.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="BudgetWise AI API",
    description="AI-powered personal finance management system",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["Transactions"])
app.include_router(budgets.router, prefix="/api/budgets", tags=["Budgets"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(goals.router, prefix="/api/goals", tags=["Goals"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI Services"])

@app.get("/")
def read_root():
    """Root endpoint - API health check"""
    return {
        "message": "BudgetWise AI API",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/api/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "database": "connected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )