"""
AI Service for Financial Insights
ai_service.py
"""

import os
from typing import List, Dict, Any
from anthropic import Anthropic
import pandas as pd
from datetime import datetime

class FinancialAIService:
    """Service for AI-powered financial insights using Claude"""
    
    def __init__(self, api_key: str = None):
        """Initialize with Anthropic API key"""
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"
    
    def generate_context_from_transactions(self, transactions: List[Dict]) -> str:
        """Create context summary from transaction data"""
        if not transactions:
            return "No transaction data available."
        
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        
        # Calculate key metrics
        total_spending = df['amount'].sum()
        avg_transaction = df['amount'].mean()
        category_totals = df.groupby('category')['amount'].sum().to_dict()
        
        # Get date range
        date_range = f"{df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}"
        
        # Format context
        context = f"""Financial Data Summary:
- Total transactions: {len(df)}
- Date range: {date_range}
- Total spending: ${total_spending:.2f}
- Average transaction: ${avg_transaction:.2f}
- Number of categories: {len(category_totals)}

Spending by Category:
"""
        for category, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total_spending) * 100
            context += f"  - {category}: ${amount:.2f} ({percentage:.1f}%)\n"
        
        # Recent transactions
        recent = df.nlargest(5, 'amount')
        context += "\nTop 5 Largest Transactions:\n"
        for _, row in recent.iterrows():
            context += f"  - {row['date'].strftime('%Y-%m-%d')}: {row['description']} - ${row['amount']:.2f} ({row['category']})\n"
        
        return context
    
    def chat(self, user_query: str, transactions: List[Dict], 
             conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """
        Chat with Claude about financial data
        
        Args:
            user_query: User's question
            transactions: List of transaction dictionaries
            conversation_history: Previous messages in conversation
        
        Returns:
            Dict with response and metadata
        """
        
        # Generate context from transactions
        context = self.generate_context_from_transactions(transactions)
        
        # Build system prompt
        system_prompt = f"""You are a helpful financial advisor AI assistant. You have access to the user's financial transaction data and can provide insights, answer questions, and offer advice.

Here is the user's financial data:

{context}

Guidelines:
- Be conversational and helpful
- Provide specific insights based on the data
- Use exact numbers from the data when possible
- Offer actionable advice
- If asked about trends, analyze patterns in the data
- If data is insufficient to answer, say so clearly
- Format currency as USD with 2 decimal places
"""
        
        # Build message history
        messages = []
        if conversation_history:
            messages.extend(conversation_history)
        
        messages.append({
            "role": "user",
            "content": user_query
        })
        
        try:
            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=messages
            )
            
            # Extract response text
            assistant_message = response.content[0].text
            
            return {
                "success": True,
                "response": assistant_message,
                "model": self.model,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            }
        
        except Exception as e:
            return {
                "success": False,
                "response": f"Error communicating with AI: {str(e)}",
                "error": str(e)
            }
    
    def generate_insights_summary(self, transactions: List[Dict]) -> str:
        """
        Generate a natural language summary of financial insights
        """
        
        context = self.generate_context_from_transactions(transactions)
        
        prompt = """Based on the financial data provided, generate a brief but insightful summary highlighting:
1. Overall spending patterns
2. Top spending categories and what they reveal
3. Any notable trends or concerns
4. One actionable recommendation

Keep it concise (3-4 sentences) and conversational."""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                system=f"You are a financial advisor. Here's the user's financial data:\n\n{context}",
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
        
        except Exception as e:
            return f"Unable to generate AI summary: {str(e)}"
    
    def explain_anomaly(self, transaction: Dict, avg_amount: float, 
                       std_amount: float) -> str:
        """
        Get AI explanation for why a transaction is anomalous
        """
        
        prompt = f"""A transaction is flagged as unusual:
- Date: {transaction['date']}
- Description: {transaction['description']}
- Amount: ${transaction['amount']:.2f}
- Category: {transaction['category']}
- Average transaction amount: ${avg_amount:.2f}
- Standard deviation: ${std_amount:.2f}

Explain in one sentence why this is unusual and if it's concerning."""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=150,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
        
        except Exception as e:
            return f"Transaction is {(transaction['amount'] / avg_amount):.1f}x higher than average"


# Alternative: OpenAI Integration (if you prefer GPT)
class FinancialAIServiceOpenAI:
    """Alternative implementation using OpenAI"""
    
    def __init__(self, api_key: str = None):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4"
    
    def chat(self, user_query: str, transactions: List[Dict],
             conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """Chat using OpenAI GPT-4"""
        
        # Similar implementation to Claude but using OpenAI format
        context = self._generate_context(transactions)
        
        messages = [
            {"role": "system", "content": f"You are a financial advisor. User's data:\n{context}"}
        ]
        
        if conversation_history:
            messages.extend(conversation_history)
        
        messages.append({"role": "user", "content": user_query})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1024
            )
            
            return {
                "success": True,
                "response": response.choices[0].message.content,
                "model": self.model
            }
        
        except Exception as e:
            return {
                "success": False,
                "response": f"Error: {str(e)}",
                "error": str(e)
            }
    
    def _generate_context(self, transactions: List[Dict]) -> str:
        """Helper to generate context - same as Claude version"""
        # (Reuse the same logic from FinancialAIService)
        pass