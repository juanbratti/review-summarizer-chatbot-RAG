import React, { useState } from 'react';
import FileUpload from './FileUpload';
import TextInput from './TextInput';
import './WelcomeScreen.css';

const WelcomeScreen = ({ onSampleQuestion }) => {
  const [activeTab, setActiveTab] = useState('text'); // Default to text input
  
  const sampleQuestions = [
    "¿Cuál es el mejor aspecto de este producto?",
    "¿Qué opinan los usuarios sobre la calidad?",
    "¿El producto tiene problemas de durabilidad?",
    "¿Cuáles son las quejas más comunes?"
  ];

  const handleUploadSuccess = (response) => {
    console.log('Upload successful:', response);
    // You could add a notification here if needed
  };

  return (
    <div className="welcome-screen">
      <div className="welcome-content">
        <h2>¡Hola! Soy REVI.AI</h2>
        <p>
          Pregúntame cualquier cosa sobre las reseñas de productos. 
          Puedo ayudarte a encontrar información específica, resumir opiniones 
          y responder preguntas sobre la experiencia de los usuarios.
        </p>
        
        {/* Upload Options Tabs */}
        <div className="upload-tabs">
          <button 
            className={`tab-btn ${activeTab === 'text' ? 'active' : ''}`}
            onClick={() => setActiveTab('text')}
          >
            📝 Pegar Texto
          </button>
          <button 
            className={`tab-btn ${activeTab === 'file' ? 'active' : ''}`}
            onClick={() => setActiveTab('file')}
          >
            📁 Subir Archivo
          </button>
        </div>

        {/* Upload Components */}
        <div className="upload-content">
          {activeTab === 'text' && (
            <TextInput onUploadSuccess={handleUploadSuccess} />
          )}
          {activeTab === 'file' && (
            <FileUpload onUploadSuccess={handleUploadSuccess} />
          )}
        </div>
        
        <div className="sample-questions">
          <h3>Preguntas de ejemplo:</h3>
          <div className="questions-grid">
            {sampleQuestions.map((question, index) => (
              <button
                key={index}
                className="sample-question-btn"
                onClick={() => onSampleQuestion(question)}
              >
                {question}
              </button>
            ))}
          </div>
        </div>
        
        <div className="tips">
          <div className="tip">
            <span className="tip-icon">💡</span>
            <span>Haz preguntas específicas para obtener mejores resultados</span>
          </div>
          <div className="tip">
            <span className="tip-icon">🔍</span>
            <span>Puedo buscar en todas las reseñas disponibles</span>
          </div>
          <div className="tip">
            <span className="tip-icon">📊</span>
            <span>Te mostraré las fuentes relevantes con cada respuesta</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WelcomeScreen; 