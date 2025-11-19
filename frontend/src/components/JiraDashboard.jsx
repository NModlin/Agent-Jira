import React, { useState } from 'react';
import { Send, Bot, User, Loader2 } from 'lucide-react';
import './JiraDashboard.css';

const JiraDashboard = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'ai',
      text: '👋 Hi! I\'m your Help Desk Assistant for project HD.\n\nI can help you:\n• Find unassigned tickets\n• Check your active queue\n• Update tickets & add comments\n\nWhat should we work on first?'
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Suggested queries for quick access
  // Suggested queries for quick access
  const suggestedQueries = [
    "Show me unassigned tickets",
    "What is on my plate?",
    "Summarize the high priority bugs",
    "Any critical tickets in HD?"
  ];

  // Function to fetch real AI response from Agent Server
  const fetchRealAiResponse = async (query, setMessages) => {
    try {
      const response = await fetch('/api/agent/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Add AI response to messages
      setMessages(prev => [...prev, {
        id: Date.now(),
        type: 'ai',
        text: data.response
      }]);
    } catch (error) {
      console.error('Error fetching AI response:', error);
      setMessages(prev => [...prev, {
        id: Date.now(),
        type: 'ai',
        text: `Sorry, I encountered an error: ${error.message}. Please make sure the Agent Server is running.`
      }]);
    }
  };

  const handleSendQuery = async (queryText) => {
    if (!queryText.trim()) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      type: 'user',
      text: queryText
    };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    // Add thinking indicator
    const thinkingId = Date.now() + 1;
    setMessages(prev => [...prev, {
      id: thinkingId,
      type: 'ai',
      text: '🤔 Thinking...',
      isThinking: true
    }]);

    // Fetch real AI response
    await fetchRealAiResponse(queryText, (updater) => {
      setMessages(prev => {
        // Remove thinking message
        const filtered = prev.filter(msg => msg.id !== thinkingId);
        // Apply the updater function
        return typeof updater === 'function' ? updater(filtered) : updater;
      });
    });

    setIsLoading(false);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    handleSendQuery(inputValue);
  };

  const handleSuggestedQuery = (query) => {
    handleSendQuery(query);
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-card">
        {/* Header */}
        <div className="dashboard-header">
          <div className="header-content">
            <Bot className="header-icon" size={32} />
            <div>
              <h1 className="header-title">HD Support Assistant</h1>
              <p className="header-subtitle">AI-Powered Team Analytics</p>
            </div>
          </div>
        </div>

        {/* Messages */}
        <div className="messages-container">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.type === 'user' ? 'message-user' : 'message-ai'}`}
            >
              <div className="message-icon">
                {message.type === 'user' ? (
                  <User size={20} />
                ) : (
                  <Bot size={20} />
                )}
              </div>
              <div className="message-content">
                <div className="message-text">
                  {message.isThinking ? (
                    <span className="thinking-text">
                      <Loader2 className="spinner" size={16} />
                      {message.text}
                    </span>
                  ) : (
                    message.text.split('\n').map((line, i) => (
                      <React.Fragment key={i}>
                        {line}
                        {i < message.text.split('\n').length - 1 && <br />}
                      </React.Fragment>
                    ))
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Suggested Queries */}
        {!isLoading && messages.length <= 2 && (
          <div className="suggested-queries">
            <p className="suggested-label">Try asking:</p>
            <div className="suggested-buttons">
              {suggestedQueries.map((query, index) => (
                <button
                  key={index}
                  onClick={() => handleSuggestedQuery(query)}
                  className="suggested-button"
                >
                  {query}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input */}
        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Ask about bugs, tasks, or team progress..."
            className="input-field"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !inputValue.trim()}
            className="send-button"
          >
            <Send size={20} />
          </button>
        </form>
      </div>
    </div>
  );
};

export default JiraDashboard;

