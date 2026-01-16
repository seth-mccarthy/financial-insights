// components/ChatInterface.tsx
import React, { useState, FormEvent } from 'react';
import { ChatMessage } from '../types';

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch(
        `http://localhost:8000/api/chat?query=${encodeURIComponent(input)}`,
        { method: 'POST' }
      );

      if (!response.ok) throw new Error('Chat request failed');

      const data = await response.json();
      
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  // Format AI response with proper line breaks and bullet points
  const formatResponse = (content: string) => {
    // Split by common markdown patterns
    const lines = content.split('\n');
    
    return lines.map((line, i) => {
      // Handle bold text **text**
      line = line.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
      
      // Handle bullet points
      if (line.trim().startsWith('- ') || line.trim().startsWith('* ')) {
        return <li key={i} dangerouslySetInnerHTML={{ __html: line.slice(2) }} />;
      }
      
      // Regular paragraph
      if (line.trim()) {
        return <p key={i} dangerouslySetInnerHTML={{ __html: line }} />;
      }
      
      // Empty line
      return <br key={i} />;
    });
  };

  return (
    <div className="chat-interface">
      <h3>💬 Ask About Your Finances</h3>
      
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="chat-placeholder">
            <p>Ask me anything about your spending patterns!</p>
            <p>Examples:</p>
            <ul>
              <li>"Why did my spending spike last month?"</li>
              <li>"What are my top spending categories?"</li>
              <li>"Any unusual transactions recently?"</li>
            </ul>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div key={index} className={`message ${msg.role}`}>
              <div className="message-content">
                {msg.role === 'assistant' ? (
                  <div className="formatted-response">
                    {formatResponse(msg.content)}
                  </div>
                ) : (
                  msg.content
                )}
              </div>
              <div className="message-time">
                {msg.timestamp.toLocaleTimeString()}
              </div>
            </div>
          ))
        )}
        {loading && (
          <div className="message assistant">
            <div className="message-content typing">Thinking...</div>
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question about your finances..."
          className="chat-input"
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()} className="chat-send">
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;