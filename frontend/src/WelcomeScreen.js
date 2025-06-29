import React from 'react';
import './WelcomeScreen.css';

const WelcomeScreen = ({ onSampleQuestion }) => {
  const sampleQuestions = [
    "¿Cuál es el mejor aspecto de este producto?",
    "¿Qué opinan los usuarios sobre la calidad?",
    "¿El producto tiene problemas de durabilidad?",
    "¿Cuáles son las quejas más comunes?"
  ];

  return (
    <div className="welcome-screen">
      <div className="welcome-content">
        <h2>¡Hola! Soy REVI.AI</h2>
        <p>
          Pregúntame cualquier cosa sobre las reseñas de productos. 
          Puedo ayudarte a encontrar información específica, resumir opiniones 
          y responder preguntas sobre la experiencia de los usuarios.
        </p>
        
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