import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from dateutil.relativedelta import relativedelta
import json

from . import models as ai_models
from ..transactions import models as transaction_models
from ..transactions import schemas as transaction_schemas
from ..auth.models import User
from ..audit.service import create_audit_log

logger = logging.getLogger(__name__)

class AIService:
    """Service class for AI-powered financial insights"""
    
    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id
    
    # Core AI Analysis Methods
    
    def analyze_spending_patterns(self, months: int = 12) -> Dict[str, Any]:
        """Analyze spending patterns and generate insights"""
        logger.info(f"Analyzing spending patterns for user {self.user_id}")
        
        # Get transactions for the specified period
        end_date = datetime.utcnow()
        start_date = end_date - relativedelta(months=months)
        
        transactions = self._get_transactions(start_date, end_date)
        
        if not transactions:
            return {"insights": [], "summary": "No transaction data available for analysis"}
        
        # Convert to DataFrame for analysis
        df = self._prepare_transaction_data(transactions)
        
        # Generate insights
        insights = []
        
        # 1. Monthly spending trends
        monthly_spending = self._analyze_monthly_spending(df)
        insights.append({
            "type": "spending_trend",
            "data": monthly_spending,
            "summary": f"Spending trends over the last {months} months"
        })
        
        # 2. Category analysis
        category_insights = self._analyze_categories(df)
        insights.extend(category_insights)
        
        # 3. Anomaly detection
        anomalies = self._detect_anomalies(df)
        if anomalies:
            insights.append({
                "type": "spending_anomalies",
                "data": anomalies,
                "summary": f"Detected {len(anomalies)} unusual transactions"
            })
        
        # 4. Recurring payments
        recurring = self._identify_recurring_payments(transactions)
        if recurring:
            insights.append({
                "type": "recurring_payments",
                "data": recurring,
                "summary": f"Identified {len(recurring)} potential recurring payments"
            })
        
        # 5. Savings opportunities
        savings = self._identify_savings_opportunities(df)
        if savings:
            insights.append({
                "type": "savings_opportunities",
                "data": savings,
                "summary": f"Found {len(savings)} potential savings opportunities"
            })
        
        # Create a summary
        total_spent = df[df['amount'] < 0]['amount'].sum() * -1
        avg_monthly_spend = total_spent / months
        
        summary = {
            "total_spent": total_spent,
            "avg_monthly_spend": avg_monthly_spend,
            "top_category": df[df['amount'] < 0].groupby('category')['amount'].sum().idxmax(),
            "insights_generated": len(insights)
        }
        
        return {"insights": insights, "summary": summary}
    
    def predict_future_spending(self, months: int = 6) -> Dict[str, Any]:
        """Predict future spending based on historical data"""
        logger.info(f"Predicting future spending for user {self.user_id}")
        
        # Get historical data (2x the prediction period for better accuracy)
        historical_months = max(12, months * 2)  # At least 12 months
        end_date = datetime.utcnow()
        start_date = end_date - relativedelta(months=historical_months)
        
        transactions = self._get_transactions(start_date, end_date)
        
        if not transactions:
            return {"predictions": [], "confidence": 0, "message": "Insufficient data for prediction"}
        
        # Convert to DataFrame and prepare time series data
        df = self._prepare_transaction_data(transactions)
        monthly_spending = df[df['amount'] < 0].groupby(pd.Grouper(key='date', freq='M'))['amount'].sum().abs()
        
        if len(monthly_spending) < 6:  # Need at least 6 months of data
            return {
                "predictions": [],
                "confidence": 0,
                "message": "Insufficient historical data (need at least 6 months)"
            }
        
        # Simple moving average prediction (can be replaced with more sophisticated models)
        window_size = min(3, len(monthly_spending) // 2)  # Adjust window size based on available data
        predictions = monthly_spending.rolling(window=window_size).mean().iloc[-window_size:].mean()
        
        # Add some seasonality (simplified)
        predictions = [predictions * (1 + (i % 3 - 1) * 0.1) for i in range(months)]
        
        # Generate prediction dates
        last_date = monthly_spending.index[-1]
        prediction_dates = [last_date + relativedelta(months=i+1) for i in range(months)]
        
        # Calculate confidence based on data quality and quantity
        confidence = min(0.9, 0.5 + 0.1 * len(monthly_spending))  # 50% + 10% per month, capped at 90%
        
        return {
            "predictions": [{"date": d.strftime("%Y-%m"), "amount": float(p)} 
                           for d, p in zip(prediction_dates, predictions)],
            "confidence": confidence,
            "message": f"Prediction based on {len(monthly_spending)} months of historical data"
        }
    
    def detect_anomalies(self, months: int = 6) -> List[Dict[str, Any]]:
        """Detect anomalous transactions"""
        logger.info(f"Detecting anomalies for user {self.user_id}")
        
        end_date = datetime.utcnow()
        start_date = end_date - relativedelta(months=months)
        
        transactions = self._get_transactions(start_date, end_date)
        
        if not transactions:
            return []
        
        df = self._prepare_transaction_data(transactions)
        
        # Only consider expense transactions for anomaly detection
        expense_df = df[df['amount'] < 0].copy()
        
        if len(expense_df) < 10:  # Need a minimum number of transactions
            return []
        
        # Prepare features for anomaly detection
        features = expense_df[['amount_abs', 'days_since_last']].fillna(0)
        
        # Standardize features
        scaler = StandardScaler()
        X = scaler.fit_transform(features)
        
        # Train isolation forest model
        clf = IsolationForest(contamination=0.1, random_state=42)
        clf.fit(X)
        
        # Predict anomalies
        is_anomaly = clf.predict(X) == -1
        anomalies = expense_df[is_anomaly].to_dict('records')
        
        # Format results
        result = []
        for anomaly in anomalies:
            result.append({
                "transaction_id": int(anomaly['id']),
                "date": anomaly['date'].strftime("%Y-%m-%d"),
                "description": anomaly['description'],
                "amount": float(anomaly['amount']),
                "category": anomaly.get('category', 'Uncategorized'),
                "reason": "Unusual spending pattern detected"
            })
        
        return result
    
    def categorize_transactions(self, transaction_ids: List[int] = None) -> Dict[str, Any]:
        """Categorize transactions using AI"""
        logger.info(f"Categorizing transactions for user {self.user_id}")
        
        # Get uncategorized transactions or specific ones if IDs are provided
        query = self.db.query(transaction_models.Transaction).filter(
            transaction_models.Transaction.user_id == self.user_id
        )
        
        if transaction_ids:
            query = query.filter(transaction_models.Transaction.id.in_(transaction_ids))
        else:
            # Get uncategorized or potentially miscategorized transactions
            query = query.filter(
                (transaction_models.Transaction.category == None) |
                (transaction_models.Transaction.category == 'Uncategorized')
            )
        
        transactions = query.all()
        
        if not transactions:
            return {"categorized": 0, "message": "No transactions to categorize"}
        
        # In a real implementation, this would use an AI/ML model
        # For now, we'll use a simple rule-based approach
        categorized = 0
        for tx in transactions:
            if not tx.category or tx.category == 'Uncategorized':
                # Simple keyword matching (in a real app, use a proper ML model)
                desc = tx.description.lower()
                
                if any(word in desc for word in ['netflix', 'spotify', 'disney', 'hulu']):
                    tx.category = 'Entertainment'
                elif any(word in desc for word in ['uber', 'lyft', 'taxi', 'train', 'bus']):
                    tx.category = 'Transportation'
                elif any(word in desc for word in ['mcdonalds', 'starbucks', 'restaurant', 'cafe']):
                    tx.category = 'Food & Dining'
                elif any(word in desc for word in ['walmart', 'target', 'amazon']):
                    tx.category = 'Shopping'
                elif any(word in desc for word in ['electric', 'water', 'gas', 'utility']):
                    tx.category = 'Utilities'
                else:
                    tx.category = 'Miscellaneous'
                
                categorized += 1
        
        self.db.commit()
        
        return {
            "categorized": categorized,
            "message": f"Successfully categorized {categorized} transactions"
        }
    
    # Helper Methods
    
    def _get_transactions(self, start_date: datetime, end_date: datetime):
        """Helper method to get transactions within a date range"""
        return self.db.query(transaction_models.Transaction).filter(
            transaction_models.Transaction.user_id == self.user_id,
            transaction_models.Transaction.date >= start_date,
            transaction_models.Transaction.date <= end_date
        ).all()
    
    def _prepare_transaction_data(self, transactions):
        """Convert transactions to a pandas DataFrame and add derived features"""
        import pandas as pd
        
        data = [{
            'id': tx.id,
            'date': tx.date,
            'description': tx.description,
            'amount': float(tx.amount),
            'amount_abs': abs(float(tx.amount)),
            'category': tx.category,
            'type': 'expense' if tx.amount < 0 else 'income'
        } for tx in transactions]
        
        df = pd.DataFrame(data)
        
        if not df.empty:
            # Sort by date
            df = df.sort_values('date')
            
            # Add time-based features
            df['month'] = df['date'].dt.to_period('M')
            df['day_of_week'] = df['date'].dt.dayofweek
            df['is_weekend'] = df['day_of_week'].isin([5, 6])
            
            # Days since last transaction
            df['days_since_last'] = df['date'].diff().dt.days
        
        return df
    
    def _analyze_monthly_spending(self, df):
        """Analyze monthly spending patterns"""
        if df.empty:
            return {}
        
        # Group by month and sum amounts
        monthly = df[df['amount'] < 0].groupby('month')['amount'].sum().abs()
        
        # Calculate statistics
        avg_spend = monthly.mean()
        max_spend = monthly.max()
        min_spend = monthly.min()
        
        # Calculate trend (simple linear regression)
        if len(monthly) > 1:
            x = np.arange(len(monthly))
            y = monthly.values
            z = np.polyfit(x, y, 1)
            trend = "increasing" if z[0] > 0 else "decreasing" if z[0] < 0 else "stable"
        else:
            trend = "insufficient_data"
        
        return {
            "average_monthly_spend": float(avg_spend),
            "max_monthly_spend": float(max_spend),
            "min_monthly_spend": float(min_spend),
            "trend": trend,
            "data": [{"month": str(m), "amount": float(a)} for m, a in zip(monthly.index, monthly.values)]
        }
    
    def _analyze_categories(self, df):
        """Analyze spending by category"""
        if df.empty:
            return []
        
        insights = []
        
        # Get top spending categories
        expenses = df[df['amount'] < 0]
        if not expenses.empty:
            category_spending = expenses.groupby('category')['amount'].sum().abs().sort_values(ascending=False)
            
            # Top category insight
            if not category_spending.empty:
                top_category = category_spending.index[0]
                top_amount = category_spending.iloc[0]
                total_spent = category_spending.sum()
                percentage = (top_amount / total_spent) * 100
                
                insights.append({
                    "type": "top_spending_category",
                    "category": top_category,
                    "amount": float(top_amount),
                    "percentage": float(percentage),
                    "summary": f"{top_category} is your top spending category at {percentage:.1f}% of total expenses"
                })
            
            # Category distribution
            category_dist = category_spending.to_dict()
            insights.append({
                "type": "category_distribution",
                "data": [{"category": k, "amount": float(v)} for k, v in category_dist.items()],
                "summary": f"Spending distribution across {len(category_dist)} categories"
            })
        
        return insights
    
    def _detect_anomalies(self, df):
        """Detect anomalous transactions"""
        if len(df) < 10:  # Need a minimum number of transactions
            return []
        
        # Simple anomaly detection: transactions > 3 standard deviations from the mean
        expenses = df[df['amount'] < 0]['amount'].abs()
        
        if len(expenses) < 5:  # Need at least 5 expenses
            return []
        
        mean = expenses.mean()
        std = expenses.std()
        
        if std == 0:  # All amounts are the same
            return []
        
        threshold = mean + (3 * std)
        anomalies = df[(df['amount'].abs() > threshold) & (df['amount'] < 0)]
        
        return anomalies.to_dict('records')
    
    def _identify_recurring_payments(self, transactions):
        """Identify potential recurring payments"""
        # Group transactions by description and amount
        from collections import defaultdict
        
        # Group similar transactions
        transaction_groups = defaultdict(list)
        for tx in transactions:
            if tx.amount < 0:  # Only consider expenses
                # Normalize description (remove numbers, special chars, etc.)
                normalized_desc = ''.join(c for c in tx.description.lower() if c.isalpha() or c.isspace())
                key = (normalized_desc.strip(), round(float(tx.amount), 2))
                transaction_groups[key].append(tx)
        
        # Find potential recurring payments (same description/amount, regular intervals)
        recurring = []
        for (desc, amount), txs in transaction_groups.items():
            if len(txs) >= 3:  # At least 3 occurrences
                # Sort by date
                txs_sorted = sorted(txs, key=lambda x: x.date)
                dates = [tx.date for tx in txs_sorted]
                
                # Calculate days between occurrences
                deltas = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
                
                # Check if intervals are somewhat regular (within 5 days of the median)
                if len(deltas) >= 2:
                    median_interval = sorted(deltas)[len(deltas)//2]
                    regular = all(abs(d - median_interval) <= 5 for d in deltas)
                    
                    if regular and 20 <= median_interval <= 45:  # Monthly-ish
                        recurring.append({
                            "description": txs_sorted[0].description,
                            "amount": float(amount),
                            "frequency_days": median_interval,
                            "next_expected": (txs_sorted[-1].date + timedelta(days=median_interval)).strftime("%Y-%m-%d"),
                            "occurrences": len(txs)
                        })
        
        return recurring
    
    def _identify_savings_opportunities(self, df):
        """Identify potential savings opportunities"""
        opportunities = []
        
        # 1. Subscriptions with low usage
        # (In a real app, this would integrate with actual usage data)
        
        # 2. High-fee transactions
        fees = df[df['description'].str.contains('fee|charge|penalty', case=False, na=False)]
        if not fees.empty:
            total_fees = fees['amount'].sum()
            if total_fees < -10:  # More than $10 in fees
                opportunities.append({
                    "type": "high_fees",
                    "amount_saved": float(abs(total_fees)),
                    "suggestion": "Consider switching to accounts with lower fees"
                })
        
        # 3. High spending in discretionary categories
        discretionary_cats = ['Dining', 'Entertainment', 'Shopping', 'Hobbies']
        disc_spending = df[df['category'].isin(discretionary_cats) & (df['amount'] < 0)]
        if not disc_spending.empty:
            monthly_disc = disc_spending.groupby('month')['amount'].sum().abs().mean()
            if monthly_disc > 200:  # More than $200/month on discretionary
                opportunities.append({
                    "type": "high_discretionary_spending",
                    "monthly_amount": float(monthly_disc),
                    "suggestion": "Consider setting a monthly budget for discretionary spending"
                })
        
        return opportunities
