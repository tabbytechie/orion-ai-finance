from fastapi import APIRouter, Depends
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/ai",
    tags=["ai"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/insights")
def get_ai_insights():
    """
    (Placeholder) Generate AI-powered insights for the user's transactions.
    """
    return {"message": "AI insights are not yet implemented."}