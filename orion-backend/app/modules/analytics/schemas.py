"""
Pydantic Schemas for the Analytics Module

This file defines the Pydantic models used for data serialization and
documentation in the analytics-related API endpoints. These schemas represent
the structure of the data returned by the analytics services.
"""

from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime

class SpendingByCategory(BaseModel):
    """Represents the total spending for a single category."""
    category: str = Field(..., description="The name of the category.", example="Groceries")
    total: float = Field(..., description="The total amount spent in this category.", example=450.75)

class AnalyticsOverview(BaseModel):
    """Schema for the financial overview analytics."""
    total_income: float = Field(..., description="Total income over the period.", example=6000.00)
    total_expense: float = Field(..., description="Total expenses over the period.", example=2500.50)
    net_balance: float = Field(..., description="Net financial balance (income - expense).", example=3499.50)
    spending_by_category: List[SpendingByCategory] = Field(
        ...,
        description="A breakdown of spending across different categories."
    )

class SpendingForecast(BaseModel):
    """Schema for the spending forecast."""
    forecasted_next_month_spending: float = Field(
        ...,
        description="The AI-powered forecast for next month's total spending.",
        example=2750.00
    )
    confidence_interval_upper: float = Field(
        ...,
        description="The upper bound of the forecast's confidence interval.",
        example=2900.00
    )
    confidence_interval_lower: float = Field(
        ...,
        description="The lower bound of the forecast's confidence interval.",
        example=2600.00
    )

class TrendPoint(BaseModel):
    """A single data point in a time-series trend."""
    date: datetime = Field(..., description="The date for this data point.")
    amount: float = Field(..., description="The aggregated amount for this data point.")

class SpendingTrend(BaseModel):
    """Schema for spending trends over time."""
    trend: List[TrendPoint] = Field(..., description="A list of data points representing the trend.")