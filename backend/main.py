"""
Financial Insights Platform - FastAPI Backend
main.py
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
from datetime import datetime
import io
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Financial Insights API")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class Transaction(BaseModel):
    date: str
    description: str
    amount: float
    category: str

class SpendingInsight(BaseModel):
    category: str
    total: float
    percentage: float
    trend: str

class AnomalyAlert(BaseModel):
    date: str
    description: str
    amount: float
    reason: str

class InsightsResponse(BaseModel):
    total_spending: float
    top_categories: List[SpendingInsight]
    anomalies: List[AnomalyAlert]
    monthly_average: float

# In-memory storage (replace with database later)
transactions_db: List[Transaction] = []

@app.get("/")
def root():
    return {"message": "Financial Insights API", "version": "1.0.0"}

@app.post("/api/upload")
async def upload_csv(file: UploadFile = File(...)):
    """Upload and process CSV file with financial transactions"""
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    try:
        # Read CSV
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Validate required columns
        required_columns = ['date', 'description', 'amount', 'category']
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(
                status_code=400,
                detail=f"CSV must contain columns: {required_columns}"
            )
        
        # Clean and process data
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = df['amount'].abs()  # Ensure positive amounts
        
        # Store in memory (replace with DB insert later)
        transactions_db.clear()
        for _, row in df.iterrows():
            transactions_db.append(Transaction(
                date=row['date'].strftime('%Y-%m-%d'),
                description=row['description'],
                amount=float(row['amount']),
                category=row['category']
            ))
        
        return {
            "message": "File uploaded successfully",
            "transactions_count": len(transactions_db)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get("/api/transactions", response_model=List[Transaction])
def get_transactions(limit: int = 100):
    """Get all transactions"""
    return transactions_db[:limit]

@app.get("/api/insights", response_model=InsightsResponse)
def get_insights():
    """Generate financial insights from transactions"""
    
    if not transactions_db:
        raise HTTPException(status_code=400, detail="No transactions available")
    
    # Convert to DataFrame for analysis
    df = pd.DataFrame([t.dict() for t in transactions_db])
    df['date'] = pd.to_datetime(df['date'])
    
    # Calculate total spending
    total_spending = df['amount'].sum()
    
    # Top categories
    category_totals = df.groupby('category')['amount'].sum().sort_values(ascending=False)
    top_categories = [
        SpendingInsight(
            category=cat,
            total=float(amount),
            percentage=float(amount / total_spending * 100),
            trend="stable"  # TODO: Calculate actual trend
        )
        for cat, amount in category_totals.head(5).items()
    ]
    
    # Detect anomalies (simple threshold-based)
    mean_amount = df['amount'].mean()
    std_amount = df['amount'].std()
    threshold = mean_amount + (2 * std_amount)
    
    anomalies_df = df[df['amount'] > threshold]
    anomalies = [
        AnomalyAlert(
            date=row['date'].strftime('%Y-%m-%d'),
            description=row['description'],
            amount=float(row['amount']),
            reason=f"Unusually high transaction (${row['amount']:.2f} vs avg ${mean_amount:.2f})"
        )
        for _, row in anomalies_df.iterrows()
    ]
    
    # Monthly average
    df['month'] = df['date'].dt.to_period('M')
    monthly_avg = df.groupby('month')['amount'].sum().mean()
    
    return InsightsResponse(
        total_spending=float(total_spending),
        top_categories=top_categories,
        anomalies=anomalies[:5],  # Limit to top 5
        monthly_average=float(monthly_avg)
    )

@app.get("/api/insights/summary")
def get_ai_insights_summary():
    """Get AI-generated summary of financial insights"""
    
    if not transactions_db:
        raise HTTPException(status_code=400, detail="No transactions available")
    
    try:
        from ai_service import FinancialAIService
        ai_service = FinancialAIService()
        
        transactions_dict = [t.dict() for t in transactions_db]
        summary = ai_service.generate_insights_summary(transactions_dict)
        
        return {
            "summary": summary,
            "generated_at": datetime.now().isoformat()
        }
    
    except ImportError:
        return {
            "summary": "AI insights unavailable. Please configure ANTHROPIC_API_KEY.",
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")

@app.post("/api/chat")
async def chat_with_ai(query: str):
    """Chat with AI about financial data"""
    
    if not transactions_db:
        raise HTTPException(status_code=400, detail="No transactions available")
    
    try:
        # Check if API key is configured
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key or api_key == "your-key-here-replace-this":
            raise HTTPException(
                status_code=500,
                detail="ANTHROPIC_API_KEY not configured. Please add your API key to backend/.env file"
            )
        
        # Initialize AI service
        from ai_service import FinancialAIService
        ai_service = FinancialAIService()
        
        # Convert transactions to dict format
        transactions_dict = [t.dict() for t in transactions_db]
        
        # Get AI response
        result = ai_service.chat(
            user_query=query,
            transactions=transactions_dict
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["response"])
        
        return {
            "query": query,
            "response": result["response"],
            "model": result.get("model"),
            "usage": result.get("usage")
        }
    
    except ImportError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"AI service not available. Error: {str(e)}"
        )
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        # Log the full error for debugging
        print(f"Error in chat endpoint: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)