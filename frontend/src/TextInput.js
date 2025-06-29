import React, { useState } from 'react';
import './TextInput.css';

const TextInput = ({ onUploadSuccess }) => {
  const [reviewText, setReviewText] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!reviewText.trim()) {
      setError('Por favor, ingresa algunas reseñas');
      return;
    }

    setIsUploading(true);
    setError('');

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/upload-text/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          reviews: reviewText
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error al procesar las reseñas');
      }

      const result = await response.json();
      onUploadSuccess(result);
      setReviewText('');
      
    } catch (error) {
      console.error('Upload error:', error);
      setError(error.message || 'Error al subir las reseñas');
    } finally {
      setIsUploading(false);
    }
  };

  const handleClear = () => {
    setReviewText('');
    setError('');
  };

  return (
    <div className="text-input-container">
      <div className="text-input-header">
        <h3>📝 Pegar Reseñas como Texto</h3>
        <p>Copia y pega las reseñas directamente en el área de texto</p>
      </div>
      
      <form onSubmit={handleSubmit} className="text-input-form">
        <div className="textarea-container">
          <textarea
            value={reviewText}
            onChange={(e) => setReviewText(e.target.value)}
            placeholder="Pega aquí las reseñas... Cada reseña puede estar en una línea separada o separadas por párrafos."
            className="review-textarea"
            rows={8}
            disabled={isUploading}
          />
          <div className="textarea-footer">
            <span className="char-count">
              {reviewText.length} caracteres
            </span>
            {reviewText && (
              <button
                type="button"
                onClick={handleClear}
                className="clear-btn"
                disabled={isUploading}
              >
                Limpiar
              </button>
            )}
          </div>
        </div>

        {error && (
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            {error}
          </div>
        )}

        <button
          type="submit"
          className="submit-btn"
          disabled={isUploading || !reviewText.trim()}
        >
          {isUploading ? (
            <>
              <span className="spinner"></span>
              Procesando...
            </>
          ) : (
            <>
              <span className="upload-icon">🚀</span>
              Procesar Reseñas
            </>
          )}
        </button>
      </form>
    </div>
  );
};

export default TextInput; 