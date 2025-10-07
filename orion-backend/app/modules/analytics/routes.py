from fastapi import APIRouter, Depends
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/overview")
def get_analytics_overview():
    """
    (Placeholder) Provide an overview of spending trends and top categories.
    """
    return {"message": "Analytics overview is not yet implemented."}

@router.get("/forecast")
def get_spending_forecast():
    """
    (Placeholder) Provide a forecast of next month's spending.
    """
    return {"message": "Spending forecast is not yet implemented."}