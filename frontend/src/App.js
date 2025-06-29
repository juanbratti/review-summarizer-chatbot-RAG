import React from 'react';
import { ThemeProvider } from './ThemeContext';
import ChatInterface from './ChatInterface';
import './App.css';

function App() {
  return (
    <ThemeProvider>
      <div className="App">
        <ChatInterface />
      </div>
    </ThemeProvider>
  );
}

export default App;
