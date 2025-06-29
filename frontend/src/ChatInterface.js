import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import WelcomeScreen from './WelcomeScreen';
import ThemeToggle from './ThemeToggle';
import './ChatInterface.css';

const ChatInterface = () => {
  // State management
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showSources, setShowSources] = useState({});
  
  // Refs for auto-scroll
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle sending messages
  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage.trim(),
      timestamp: new Date()
    };

    // Add user message immediately
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      // Call your backend API
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await axios.post(`${apiUrl}/app/questions/`, {
        question: userMessage.content
      });

      // Add assistant response
      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: response.data.answer,
        timestamp: new Date(),
        sources: response.data.results || []
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      
      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: 'Lo siento, hubo un error al procesar tu pregunta. Por favor, inténtalo de nuevo.',
        timestamp: new Date(),
        isError: true
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Toggle sources visibility
  const toggleSources = (messageId) => {
    setShowSources(prev => ({
      ...prev,
      [messageId]: !prev[messageId]
    }));
  };

  // Format timestamp
  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString('es-ES', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  // Handle sample question click
  const handleSampleQuestion = (question) => {
    setInputMessage(question);
  };

  return (
    <div className="chat-interface">
      {/* Header */}
      <div className="chat-header">
        <div className="chat-title">
          <h2>REVI.AI</h2>
          <p>Pregúntame sobre productos y reseñas</p>
        </div>
        <div className="header-controls">
          <ThemeToggle />
          {messages.length > 0 && (
            <button 
              className="clear-chat-btn"
              onClick={() => setMessages([])}
              title="Nueva conversación"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M3 6h18"></path>
                <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
                <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
              </svg>
              Nueva conversación
            </button>
          )}
        </div>
      </div>

      {/* Messages Container */}
      <div className="messages-container">
        <div className="messages-wrapper">
          {messages.length === 0 ? (
            <WelcomeScreen onSampleQuestion={handleSampleQuestion} />
          ) : (
            messages.map((message) => (
            <div key={message.id} className={`message ${message.type}`}>
              <div className="message-content">
                <div className={`message-bubble ${message.type} ${message.isError ? 'error' : ''}`}>
                  <p>{message.content}</p>
                  <span className="message-time">{formatTime(message.timestamp)}</span>
                </div>
                
                {/* Sources section for assistant messages */}
                {message.type === 'assistant' && message.sources && message.sources.length > 0 && (
                  <div className="sources-section">
                    <button 
                      className="sources-toggle"
                      onClick={() => toggleSources(message.id)}
                    >
                      {showSources[message.id] ? 'Ocultar fuentes' : `Ver fuentes (${message.sources.length})`}
                    </button>
                    
                    {showSources[message.id] && (
                      <div className="sources-list">
                        {message.sources.map((source, index) => (
                          <div key={index} className="source-item">
                            <div className="source-snippet">
                              <strong>Fragmento:</strong> {source.content_snippet}
                            </div>
                            <div className="source-score">
                              Similitud: {source.similarity_score.toFixed(3)}
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
            ))
          )}
          
          {/* Loading indicator */}
          {isLoading && (
            <div className="message assistant">
              <div className="message-content">
                <div className="message-bubble assistant typing">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="input-container">
        <div className="input-wrapper">
          <textarea
            ref={textareaRef}
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Pregúntame sobre las reseñas..."
            rows="1"
            disabled={isLoading}
          />
          <button 
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isLoading}
            className="send-button"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22,2 15,22 11,13 2,9 22,2"></polygon>
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface; 