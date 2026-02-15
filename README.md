# Financial Insights Platform

AI-powered financial analysis platform built with **FastAPI** (Python) and **React + TypeScript**.

## Project Structure

```
financial-insights/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Database models
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables
├── frontend/
│   ├── src/
│   │   ├── App.tsx         # Main React component
│   │   ├── types.ts        # TypeScript types
│   │   ├── components/
│   │   │   ├── FileUpload.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   └── ChatInterface.tsx
│   │   └── App.css
│   ├── package.json
│   └── vite.config.ts
└── sample_transactions.csv
```

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Claude API key (get from [console.anthropic.com](https://console.anthropic.com/))

### Backend Setup

```bash
# Create virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file and add your API key
cp .env.example .env
# Edit .env and add: ANTHROPIC_API_KEY=sk-ant-your-key-here

# Test AI integration (optional but recommended)
python test_ai.py

# Run the server
python -m uvicorn main:app --reload
```

Backend will run at: `http://localhost:8000`
API docs: `http://localhost:8000/docs`

### Frontend Setup

```bash
# Install dependencies
cd frontend
npm install

# Run development server
npm run dev
```

Frontend will run at: `http://localhost:5173`

## Features

### Current Features
- ✅ CSV upload and processing
- ✅ Spending insights and analytics
- ✅ Category breakdown with visualizations
- ✅ Anomaly detection (unusual transactions)
- ✅ Monthly spending averages
- ✅ Interactive dashboard
- ✅ **AI-powered chat interface** (Claude API)
- ✅ **Natural language financial insights**
- ✅ **Context-aware spending analysis**

## Screenshots

### File Upload
![Upload](screenshots/file-upload.png)

### Dashboard Overview
![Dashboard](screenshots/dashboard.png)

### AI Chat
![AI Chat](screenshots/ai-chat.png)

### Anomaly Detection  
![Anomalies](screenshots/anomaly-detection.png)

### Coming Soon
- 🔄 Time-series forecasting (Prophet/statsmodels)
- 🔄 Trend analysis with ML
- 🔄 Budget recommendations
- 🔄 PostgreSQL database integration
- 🔄 User authentication
- 🔄 Conversation history storage

## Testing with Sample Data

Use the included `sample_transactions.csv` to test the application:

1. Start both backend and frontend
2. Upload `sample_transactions.csv` through the UI
3. View generated insights and anomalies

## Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- Pandas - Data processing
- SQLAlchemy - Database ORM
- Prophet - Time-series forecasting (coming soon)
- Anthropic/OpenAI SDK - AI integration (coming soon)

**Frontend:**
- React 18 - UI framework
- TypeScript - Type safety
- Vite - Build tool
- Recharts - Data visualizations
- CSS3 - Styling

## API Endpoints

### `POST /api/upload`
Upload CSV file with transaction data

**Expected CSV format:**
```csv
date,description,amount,category
2024-01-01,Grocery Store,50.00,Groceries
```

### `GET /api/transactions`
Retrieve all transactions (limit: 100)

### `GET /api/insights`
Get financial insights including:
- Total spending
- Top categories
- Anomalies
- Monthly average

### `POST /api/chat`
Chat with AI about your financial data

**Example queries:**
- "Why did my spending spike last month?"
- "What are my top spending categories?"
- "Any unusual transactions?"
- "How can I reduce my dining expenses?"

**Response:**
```json
{
  "query": "Why did my spending spike?",
  "response": "Your spending increased primarily due to...",
  "model": "claude-sonnet-4-20250514",
  "usage": {"input_tokens": 450, "output_tokens": 120}
}
```

### `GET /api/insights/summary`
Get AI-generated natural language summary of your finances

## Environment Variables

Create a `.env` file in the backend directory:

```env
# AI API Keys (choose one)
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Database (optional, defaults to SQLite)
DATABASE_URL=postgresql://user:pass@localhost/financial_insights
```

## License

MIT License - Feel free to use this project for your portfolio.
