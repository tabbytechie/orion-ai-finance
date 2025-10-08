from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user
from . import service, models, schemas
from ..auth.models import User

router = APIRouter(prefix="/ai-insights", tags=["ai-insights"])

# Helper function to get AI service instance
def get_ai_service(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> service.AIService:
    return service.AIService(db=db, user_id=current_user.id)

@router.get("/spending-patterns", response_model=Dict[str, Any])
async def get_spending_patterns(
    months: int = 12,
    ai_service: service.AIService = Depends(get_ai_service)
):
    """
    Analyze spending patterns and generate insights
    
    - **months**: Number of months of data to analyze (default: 12)
    """
    try:
        return ai_service.analyze_spending_patterns(months=months)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing spending patterns: {str(e)}"
        )

@router.get("/predict-spending", response_model=Dict[str, Any])
async def predict_future_spending(
    months: int = 6,
    ai_service: service.AIService = Depends(get_ai_service)
):
    """
    Predict future spending based on historical data
    
    - **months**: Number of months to predict (default: 6)
    """
    try:
        return ai_service.predict_future_spending(months=months)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error predicting future spending: {str(e)}"
        )

@router.get("/anomalies", response_model=List[Dict[str, Any]])
async def get_anomalies(
    months: int = 6,
    ai_service: service.AIService = Depends(get_ai_service)
):
    """
    Detect anomalous transactions
    
    - **months**: Number of months of data to analyze (default: 6)
    """
    try:
        return ai_service.detect_anomalies(months=months)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error detecting anomalies: {str(e)}"
        )

@router.post("/categorize", response_model=Dict[str, Any])
async def categorize_transactions(
    transaction_ids: Optional[List[int]] = None,
    background_tasks: BackgroundTasks = None,
    ai_service: service.AIService = Depends(get_ai_service)
):
    """
    Categorize transactions using AI
    
    - **transaction_ids**: List of transaction IDs to categorize (if not provided, all uncategorized transactions will be processed)
    """
    try:
        if background_tasks:
            # Run in background if background_tasks is provided
            background_tasks.add_task(
                ai_service.categorize_transactions,
                transaction_ids=transaction_ids
            )
            return {"status": "processing", "message": "Categorization started in the background"}
        else:
            # Run synchronously
            return ai_service.categorize_transactions(transaction_ids=transaction_ids)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error categorizing transactions: {str(e)}"
        )

@router.get("/recurring-payments", response_model=List[Dict[str, Any]])
async def get_recurring_payments(
    months: int = 12,
    ai_service: service.AIService = Depends(get_ai_service)
):
    """
    Identify potential recurring payments
    
    - **months**: Number of months of data to analyze (default: 12)
    """
    try:
        # This is a simplified version - in a real app, this would be a separate method in the service
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=months*30)
        
        # Get transactions and convert to DataFrame
        transactions = ai_service._get_transactions(start_date, end_date)
        if not transactions:
            return []
            
        return ai_service._identify_recurring_payments(transactions)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error identifying recurring payments: {str(e)}"
        )

@router.get("/savings-opportunities", response_model=List[Dict[str, Any]])
async def get_savings_opportunities(
    months: int = 6,
    ai_service: service.AIService = Depends(get_ai_service)
):
    """
    Identify potential savings opportunities
    
    - **months**: Number of months of data to analyze (default: 6)
    """
    try:
        # This is a simplified version - in a real app, this would be a separate method in the service
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=months*30)
        
        # Get transactions and convert to DataFrame
        transactions = ai_service._get_transactions(start_date, end_date)
        if not transactions:
            return []
            
        df = ai_service._prepare_transaction_data(transactions)
        return ai_service._identify_savings_opportunities(df)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error identifying savings opportunities: {str(e)}"
        )

@router.get("/financial-health", response_model=Dict[str, Any])
async def get_financial_health(
    ai_service: service.AIService = Depends(get_ai_service)
):
    """
    Get an overall financial health score and insights
    """
    try:
        # Get spending patterns
        spending = ai_service.analyze_spending_patterns(months=12)
        
        # Get savings rate (simplified)
        income = 0
        expenses = 0
        
        # Get transactions for the last 3 months
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=90)
        transactions = ai_service._get_transactions(start_date, end_date)
        
        if transactions:
            df = ai_service._prepare_transaction_data(transactions)
            if not df.empty:
                income = df[df['amount'] > 0]['amount'].sum()
                expenses = abs(df[df['amount'] < 0]['amount'].sum())
        
        # Calculate savings rate (simplified)
        savings_rate = ((income - expenses) / income * 100) if income > 0 else 0
        
        # Calculate financial health score (0-100)
        # This is a simplified version - in a real app, this would consider many more factors
        health_score = min(100, max(0, 50 + (savings_rate * 0.5)))
        
        # Generate insights
        insights = []
        
        if savings_rate < 10:
            insights.append({
                "type": "low_savings_rate",
                "severity": "high",
                "message": f"Your savings rate is {savings_rate:.1f}%. Consider increasing your savings rate to at least 20% for better financial health."
            })
        
        # Add any spending pattern insights
        if 'insights' in spending:
            for insight in spending['insights']:
                if insight['type'] == 'top_spending_category':
                    insights.append({
                        "type": "spending_insight",
                        "severity": "medium",
                        "message": f"Your top spending category is {insight['category']}, accounting for {insight['percentage']:.1f}% of your expenses."
                    })
        
        return {
            "score": round(health_score, 1),
            "savings_rate": round(savings_rate, 1),
            "income_last_3m": income,
            "expenses_last_3m": expenses,
            "insights": insights,
            "recommendations": [
                "Review your monthly subscriptions and cancel unused services",
                "Set up automatic transfers to savings on payday",
                "Create a budget for discretionary spending"
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating financial health: {str(e)}"
        )
