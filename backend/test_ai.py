"""
Test script for AI integration
test_ai.py

Run this to verify your API key is working:
python test_ai.py
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_claude_api():
    """Test Claude API integration"""
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found in .env file")
        print("   Please add your API key to .env:")
        print("   ANTHROPIC_API_KEY=sk-ant-...")
        return False
    
    print(f"✅ API key found: {api_key[:20]}...")
    
    try:
        from anthropic import Anthropic
        print("✅ Anthropic package imported successfully")
        
        client = Anthropic(api_key=api_key)
        print("✅ Claude client initialized")
        
        # Test API call
        print("\n🤖 Testing API call...")
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=100,
            messages=[
                {"role": "user", "content": "Say 'API test successful!' if you can read this."}
            ]
        )
        
        print(f"✅ API Response: {response.content[0].text}")
        print(f"   Model: {response.model}")
        print(f"   Tokens used: {response.usage.input_tokens} in, {response.usage.output_tokens} out")
        
        return True
        
    except ImportError:
        print("❌ Anthropic package not installed")
        print("   Run: pip install anthropic")
        return False
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_financial_ai_service():
    """Test the FinancialAIService class"""
    
    print("\n" + "="*50)
    print("Testing FinancialAIService")
    print("="*50 + "\n")
    
    try:
        from ai_service import FinancialAIService
        
        # Sample transaction data
        sample_transactions = [
            {
                "date": "2024-01-05",
                "description": "Grocery Store",
                "amount": 85.43,
                "category": "Groceries"
            },
            {
                "date": "2024-01-10",
                "description": "Restaurant",
                "amount": 67.89,
                "category": "Dining"
            },
            {
                "date": "2024-01-15",
                "description": "Amazon Purchase",
                "amount": 450.00,
                "category": "Shopping"
            }
        ]
        
        ai_service = FinancialAIService()
        print("✅ FinancialAIService initialized")
        
        # Test chat
        print("\n🤖 Testing chat functionality...")
        result = ai_service.chat(
            user_query="What are my top spending categories?",
            transactions=sample_transactions
        )
        
        if result["success"]:
            print("✅ Chat response received:")
            print(f"   {result['response'][:200]}...")
        else:
            print(f"❌ Chat failed: {result['response']}")
            return False
        
        # Test insights summary
        print("\n📊 Testing insights summary...")
        summary = ai_service.generate_insights_summary(sample_transactions)
        print(f"✅ Summary: {summary[:200]}...")
        
        print("\n" + "="*50)
        print("✅ All tests passed!")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing FinancialAIService: {str(e)}")
        return False

if __name__ == "__main__":
    print("="*50)
    print("AI Integration Test Suite")
    print("="*50 + "\n")
    
    # Test 1: Claude API
    success = test_claude_api()
    
    if success:
        # Test 2: Financial AI Service
        test_financial_ai_service()
    else:
        print("\n⚠️  Fix the API key issue before proceeding")
        print("   Get your key from: https://console.anthropic.com/")