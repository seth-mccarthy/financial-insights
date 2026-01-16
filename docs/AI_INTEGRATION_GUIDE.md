# 🤖 AI Integration Guide (UPDATED)

Complete guide to setting up Claude API integration for the Financial Insights Platform.

## 📋 Overview

The platform uses Claude AI to:
- **Answer questions** about spending patterns in natural language
- **Generate insights** from transaction data automatically
- **Explain anomalies** with context-aware reasoning
- **Provide advice** based on spending behavior
- **Format responses** beautifully with paragraphs, lists, and emphasis

## 🔑 Getting API Keys

### Claude (Recommended) ⭐

**Why Claude?**
- Latest technology (Sonnet 4 - January 2025)
- Better at reasoning and financial analysis
- More affordable (~6x cheaper than GPT-4)
- Anthropic is a top AI company
- 200K token context window

**Steps:**
1. Go to [https://console.anthropic.com/](https://console.anthropic.com/)
2. Sign up for an account (free trial available - $5 credit)
3. Navigate to "API Keys" section
4. Click "Create Key"
5. Copy your key (starts with `sk-ant-api03-`)
6. Save it securely!

**Pricing:** ~$3 per million input tokens, $15 per million output tokens
- For this project, expect < $1 for testing/development
- 1000 chat queries ≈ $3.75

### OpenAI (Alternative)

If you prefer GPT-4:
1. Go to [https://platform.openai.com/](https://platform.openai.com/)
2. Sign up and add payment method (no free tier)
3. Navigate to API keys
4. Create new secret key
5. Copy your key (starts with `sk-`)

**Pricing:** GPT-4: $30/$60 per million tokens (10x more expensive)

## ⚙️ Setup Instructions

### 1. Install Dependencies

The Anthropic SDK is already in requirements.txt:

```bash
cd backend
# Make sure venv is activated
pip install anthropic
```

For OpenAI (optional):
```bash
pip install openai
```

### 2. Configure Environment Variables

Create `.env` file in the `backend/` directory:

```bash
# Windows
cd backend
New-Item .env

# Mac/Linux
cd backend
touch .env
```

Add your API key to `.env`:
```env
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_ACTUAL_KEY_HERE
```

**Important:**
- Never commit `.env` to git (it's in .gitignore)
- Never hardcode API keys in source code
- Replace the placeholder with your real key!

### 3. Test the Integration

Run the test script:

```bash
# Windows PowerShell
cd backend
venv\Scripts\Activate.ps1
python test_ai.py

# Mac/Linux
cd backend
source venv/bin/activate
python test_ai.py
```

You should see:
```
✅ API key found: sk-ant-api03-...
✅ Anthropic package imported successfully
✅ Claude client initialized
🤖 Testing API call...
✅ API Response: API test successful!
   Model: claude-sonnet-4-20250514
   Tokens used: X in, Y out
```

If you see errors, run the debug script:
```bash
python debug_backend.py
```

### 4. Start the Backend

```bash
uvicorn main:app --reload
```

The backend will load your API key from `.env` automatically.

## 💬 Example Queries

Try these questions with your AI chat:

### Basic Questions
- "What are my top spending categories?"
- "How much did I spend this month?"
- "Show me my largest transactions"
- "What's my average transaction amount?"

### Analysis Questions
- "Why did my spending spike in February?"
- "Am I spending too much on dining out?"
- "What's unusual about my spending pattern?"
- "Compare my grocery spending to other categories"

### Advice Questions
- "How can I reduce my spending?"
- "What should I budget for next month?"
- "Which categories should I focus on cutting?"
- "Give me tips for saving money on groceries"

### Trend Questions
- "Is my grocery spending increasing?"
- "How does this month compare to last month?"
- "What's my spending trend over time?"
- "Are there any concerning patterns?"

## 🔧 How It Works

### 1. Context Generation

When you ask a question, the AI service creates a financial summary:

```python
context = """
Financial Data Summary:
- Total transactions: 32
- Date range: 2024-01-05 to 2024-03-28
- Total spending: $3,157.23
- Average transaction: $98.66

Spending by Category:
  - Shopping: $1,675.25 (53.1%)
  - Groceries: $645.67 (20.4%)
  - Dining: $478.29 (15.1%)
  ...

Top 5 Largest Transactions:
  - 2024-03-22: Furniture Store - $890.00 (Shopping)
  - 2024-02-08: Best Buy Electronics - $450.00 (Shopping)
  ...
"""
```

### 2. AI Processing

The context + your query are sent to Claude:

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=f"You are a financial advisor. User's data:\n{context}",
    messages=[
        {"role": "user", "content": "Why did my spending spike?"}
    ]
)
```

### 3. Response Formatting

The frontend formats the AI response for better readability:
- **Bold text** for emphasis (`**text**` → bold)
- Proper paragraphs with spacing
- Bullet points as actual lists
- Line breaks between sections

Example formatted response:
> **Major Purchases:** That $890 furniture purchase was by far your largest single transaction.
>
> **Shopping Category Impact:** Your Shopping category accounts for $1,675.25 (46.4%) of total spending.
>
> **What this means:** With an average transaction of $112.98, that furniture purchase alone was nearly 8 times your typical spending.

## 🎨 Frontend Integration

The ChatInterface component handles formatting:

```typescript
// Converts AI markdown-style text to formatted HTML
const formatResponse = (content: string) => {
  // Handles **bold**, bullet points, paragraphs, line breaks
  // Makes responses look professional and easy to read
};
```

## 🚨 Troubleshooting

### "ANTHROPIC_API_KEY not found"
**Fix:**
1. Check `.env` file exists in `backend/` directory
2. Verify file contains: `ANTHROPIC_API_KEY=sk-ant-...`
3. Make sure key doesn't have quotes around it
4. Restart the backend server after adding key

```bash
# Check if .env exists
cd backend
ls .env  # Mac/Linux
dir .env # Windows

# View contents
cat .env  # Mac/Linux
type .env # Windows
```

### "Module 'anthropic' not found"
**Fix:**
```bash
pip install anthropic
```

Make sure your virtual environment is activated!

### "Rate limit exceeded"
**Fix:**
- You've used up your free credits
- Add payment method at console.anthropic.com
- Or wait for quota to reset
- Claude has generous limits (rarely hit in dev)

### "API connection failed"
**Fix:**
- Check internet connection
- Verify API key is valid at console.anthropic.com
- Check if key is expired or revoked
- Try regenerating the key

### AI responses not formatted
**Fix:**
1. Make sure you updated ChatInterface.tsx with the new formatResponse function
2. Clear browser cache (Ctrl+Shift+R)
3. Check browser console for errors

### Slow responses (5+ seconds)
**Normal!** AI inference takes 3-5 seconds. This is expected.

To improve:
- Reduce max_tokens in ai_service.py
- Cache common queries
- Add streaming (advanced)

## 📊 Monitoring API Usage

Track your usage and costs:

**Claude Console:**
1. Visit [console.anthropic.com](https://console.anthropic.com/)
2. Go to "Usage" section
3. View requests and token counts
4. Set budget alerts

**In Your App:**
The `/api/chat` endpoint returns token usage:
```json
{
  "usage": {
    "input_tokens": 450,
    "output_tokens": 120
  }
}
```

**Cost Calculation:**
- Input: 450 tokens × $3/1M = $0.00135
- Output: 120 tokens × $15/1M = $0.0018
- **Total: ~$0.003 per query**

Very affordable for development!

## 🔒 Security Best Practices

1. ✅ **Never commit `.env`** - Already in .gitignore
2. ✅ **Use environment variables** - Never hardcode keys
3. ✅ **Rotate keys regularly** - Generate new every few months
4. ✅ **Monitor usage** - Watch for unusual activity
5. ✅ **Set usage limits** - Configure budget alerts
6. ✅ **Don't share keys** - Each developer should have their own

## 🎯 Advanced Features (Optional)

### Conversation Memory

Store chat history in database for context:
```python
# In ai_service.py
conversation_history = [
    {"role": "user", "content": "What are my top categories?"},
    {"role": "assistant", "content": "Your top categories are..."},
]

result = ai_service.chat(
    user_query="Tell me more about the first one",
    transactions=transactions_dict,
    conversation_history=conversation_history  # Claude remembers!
)
```

### Streaming Responses

For real-time typing effect:
```python
# Use stream=True in Claude API
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    messages=messages
) as stream:
    for text in stream.text_stream:
        yield text  # Stream to frontend
```

### Custom Prompts

Edit the system prompt in `ai_service.py` to customize behavior:
```python
system_prompt = f"""You are a [ROLE].
Your goal is to [OBJECTIVE].

Guidelines:
- Be [TONE]
- Focus on [PRIORITY]
- Avoid [RESTRICTIONS]

User's data: {context}
"""
```

## 💡 Tips for Demos/Interviews

**Show off these features:**
1. Upload data → Instant AI insights
2. Ask complex questions like "Why did spending spike?"
3. Show formatted responses (paragraphs, bold, lists)
4. Demonstrate contextual understanding
5. Highlight cost optimization (Claude vs GPT-4)

**Talking points:**
- "I integrated Claude Sonnet 4 for natural language financial analysis"
- "The AI provides context-aware insights by analyzing transaction patterns"
- "I chose Claude over GPT-4 for superior reasoning and 85% cost savings"
- "Responses are beautifully formatted with proper structure and emphasis"
- "The system generates dynamic context from user data for each query"

## 📚 Resources

- [Anthropic API Docs](https://docs.anthropic.com/)
- [Claude Prompt Engineering](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Model Comparison](https://docs.anthropic.com/claude/docs/models-overview)
- [OpenAI API Docs](https://platform.openai.com/docs) (alternative)

## ✅ Verification Checklist

Before demoing:
- [ ] `backend/.env` has real API key
- [ ] `python test_ai.py` passes
- [ ] Backend starts without errors
- [ ] Frontend chat sends messages
- [ ] AI responses are formatted nicely
- [ ] No console errors
- [ ] Responses appear in 3-5 seconds
- [ ] Multiple queries work in sequence

---

**You're all set! Your AI integration is production-ready! 🚀**

## 📋 Overview

The platform uses AI to:
- **Answer questions** about spending patterns in natural language
- **Generate insights** from transaction data automatically
- **Explain anomalies** with context-aware reasoning
- **Provide advice** based on spending behavior

## 🔑 Getting API Keys

### Option 1: Claude (Recommended)

**Why Claude?**
- Latest technology (shows you're cutting-edge)
- Better at reasoning and analysis
- More affordable for this use case
- Anthropic is a top AI company

**Steps:**
1. Go to [https://console.anthropic.com/](https://console.anthropic.com/)
2. Sign up for an account (free trial available)
3. Navigate to "API Keys" section
4. Click "Create Key"
5. Copy your key (starts with `sk-ant-`)

**Pricing:** ~$3 per million input tokens, $15 per million output tokens
- For this project, expect < $1 for testing/development

### Option 2: OpenAI

**Steps:**
1. Go to [https://platform.openai.com/](https://platform.openai.com/)
2. Sign up and add payment method
3. Navigate to API keys
4. Create new secret key
5. Copy your key (starts with `sk-`)

**Pricing:** GPT-4: $30 per million input tokens, $60 per million output

## ⚙️ Setup Instructions

### 1. Install Dependencies

Make sure you have the Anthropic SDK installed:

```bash
cd backend
pip install anthropic
```

For OpenAI (optional):
```bash
pip install openai
```

### 2. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# Copy the example file
cp .env.example .env

# Edit with your favorite editor
nano .env
```

Add your API key:
```env
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_ACTUAL_KEY_HERE
```

### 3. Test the Integration

Start your FastAPI server:
```bash
cd backend
python main.py
```

Test the AI endpoint using curl:
```bash
# Upload sample data first
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@sample_transactions.csv"

# Test AI chat
curl -X POST "http://localhost:8000/api/chat?query=What%20are%20my%20top%20spending%20categories?"

# Get AI-generated summary
curl "http://localhost:8000/api/insights/summary"
```

## 💬 Example Queries

Try these questions with your AI chat:

### Basic Questions
- "What are my top spending categories?"
- "How much did I spend this month?"
- "Show me my largest transactions"

### Analysis Questions
- "Why did my spending spike in February?"
- "Am I spending too much on dining out?"
- "What's unusual about my spending pattern?"

### Advice Questions
- "How can I reduce my spending?"
- "What should I budget for next month?"
- "Which categories should I focus on cutting?"

### Trend Questions
- "Is my grocery spending increasing?"
- "How does this month compare to last month?"
- "What's my average monthly spending?"

## 🔧 How It Works

### 1. Context Generation

The AI service creates a financial summary:
```python
context = """
Financial Data Summary:
- Total transactions: 32
- Date range: 2024-01-05 to 2024-03-28
- Total spending: $3,157.23
- Average transaction: $98.66

Spending by Category:
  - Shopping: $1,675.25 (53.1%)
  - Groceries: $645.67 (20.4%)
  - Dining: $478.29 (15.1%)
  ...
"""
```

### 2. AI Processing

The context is sent to Claude with your query:
```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    system=f"You are a financial advisor. User's data:\n{context}",
    messages=[
        {"role": "user", "content": "Why did my spending spike?"}
    ]
)
```

### 3. Response Generation

Claude analyzes the data and responds naturally:
```
"Your spending spiked in February primarily due to two large 
purchases: a $450 electronics purchase at Best Buy and an $890 
furniture purchase. These represent 42% of that month's spending. 
Your regular expenses remained consistent."
```

## 🎨 Frontend Integration

The chat component is already set up to work with the API. Once the backend is configured, the chat will automatically work!

```typescript
// ChatInterface.tsx already handles this
const response = await fetch(
  `http://localhost:8000/api/chat?query=${encodeURIComponent(input)}`,
  { method: 'POST' }
);
```

## 🚨 Troubleshooting

### "ANTHROPIC_API_KEY not found"
- Make sure `.env` file exists in `backend/` directory
- Check that your key starts with `sk-ant-`
- Restart the FastAPI server after adding the key

### "Rate limit exceeded"
- You've hit your API quota
- Upgrade your plan or wait for quota reset
- Claude has generous free tier limits

### "Module 'anthropic' not found"
```bash
pip install anthropic
```

### AI responses are slow
- Normal! AI inference takes 2-5 seconds
- Consider adding loading indicators
- Cache common queries for better UX

## 📊 Monitoring API Usage

Track your usage in the console:
- **Claude**: [https://console.anthropic.com/](https://console.anthropic.com/)
- **OpenAI**: [https://platform.openai.com/usage](https://platform.openai.com/usage)

## 🔒 Security Best Practices

1. **Never commit `.env` file** - Already in `.gitignore`
2. **Use environment variables** - Never hardcode API keys
3. **Rotate keys regularly** - Generate new keys periodically
4. **Monitor usage** - Watch for unusual activity
5. **Set usage limits** - Configure budget alerts in console

## 🎯 Next Steps

1. **Add conversation memory** - Store chat history in database
2. **Implement caching** - Cache common queries to save costs
3. **Add rate limiting** - Prevent abuse
4. **Fine-tune prompts** - Improve response quality
5. **Add streaming** - Stream responses for better UX

## 💡 Tips for Demos/Interviews

**Show off these features:**
1. Ask complex questions like "Compare my spending this month vs last month"
2. Demonstrate natural language understanding
3. Show how AI explains anomalies contextually
4. Highlight cost optimization (Claude vs OpenAI pricing)

**Talking points:**
- "I integrated Claude's latest model for natural language financial analysis"
- "The AI provides context-aware insights by analyzing transaction patterns"
- "I chose Claude over GPT-4 for better reasoning and lower costs"
- "The system generates dynamic context from user data for each query"

## 📚 Resources

- [Anthropic API Docs](https://docs.anthropic.com/)
- [Claude Prompt Engineering](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [OpenAI API Docs](https://platform.openai.com/docs)

## ❓ Need Help?

Common issues:
- API key issues: Check console logs
- Rate limits: Monitor usage dashboard
- Response quality: Improve system prompts in `ai_service.py`