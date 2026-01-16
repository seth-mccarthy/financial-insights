// App.tsx - Main React Application
import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import Dashboard from './components/Dashboard';
import ChatInterface from './components/ChatInterface';
import { InsightsData } from './types';
import './App.css';

function App() {
  const [insights, setInsights] = useState<InsightsData | null>(null);
  const [loading, setLoading] = useState(false);

  const handleFileUploaded = async () => {
    setLoading(true);
    try {
      // Fetch insights after file upload
      const response = await fetch('http://localhost:8000/api/insights');
      if (!response.ok) throw new Error('Failed to fetch insights');
      
      const data = await response.json();
      setInsights(data);
    } catch (error) {
      console.error('Error fetching insights:', error);
      alert('Error loading insights. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>💰 Financial Insights Platform</h1>
        <p>AI-powered analysis of your spending patterns</p>
      </header>

      <main className="app-main">
        {!insights ? (
          <div className="upload-section">
            <h2>Get Started</h2>
            <p>Upload your financial data to generate insights</p>
            <FileUpload onUploadSuccess={handleFileUploaded} />
          </div>
        ) : (
          <>
            <Dashboard insights={insights} loading={loading} />
            <ChatInterface />
          </>
        )}
      </main>
    </div>
  );
}

export default App;