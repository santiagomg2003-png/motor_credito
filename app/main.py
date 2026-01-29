# app/main.py
from fastapi import FastAPI
from app.api.routes.evaluate import router as evaluate_router

app = FastAPI(
    title="Motor de Scoring de Crédito",
    version="1.0.0"    
)

app.include_router(
    evaluate_router,
    prefix="/credit",
    tags=["Evaluación de Crédito"]
)
