import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  // Estado para almacenar la pregunta y la respuesta
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [documents, setDocuments] = useState([]);
  const [showDocuments, setShowDocuments] = useState(false);
  const [chatHistory, setChatHistory] = useState([]); 
  const [showHistory, setShowHistory] = useState(false); 


  // Función para manejar el envío de la pregunta
  const handleAskQuestion = async () => {
    if (!question) return;

    setLoading(true);
    try {
      // Realizar la solicitud POST al backend
      const res = await axios.post('http://localhost:8000/app/questions/', {
        question: question,
      });

      // Almacenar la respuesta del chatbot
      setResponse(res.data.answer);
      // Almacenar los documentos de la respuesta
      setDocuments(res.data.results || []);
    } catch (error) {
      console.error('Error al enviar la pregunta:', error);
      setResponse('Lo siento, hubo un error al procesar tu pregunta.');
    } finally {
      setLoading(false);
    }
  };

  // Función para manejar el cambio del botón "Mostrar Documentos"
  const toggleDocuments = () => {
    setShowDocuments((prevState) => !prevState);
  };

  const handleShowHistory = async () => {
    try {
      const res = await axios.get('http://localhost:8000/app/history/');
      setChatHistory(res.data.history); // Almacenar el historial de chat recibido
      setShowHistory(true); // Mostrar el historial
    } catch (error) {
      console.error('Error al obtener el historial:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>¿Qué quieres saber?</h1>

        <div className="chat-container">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Escribe tu pregunta..."
            rows="4"
            cols="50"
          ></textarea>
          <button onClick={handleAskQuestion} disabled={loading}>
            {loading ? 'Enviando...' : 'Preguntar'}
          </button>

          {response && (
            <div className="response">
              <h3>Respuesta:</h3>
              <p>{response}</p>
            </div>
          )}

{documents.length > 0 && (
            <div>
              <button onClick={toggleDocuments}>
                {showDocuments ? 'Ocultar Documentos' : 'Mostrar Documentos'}
              </button>

              {showDocuments && (
                <div className="documents">
                  <h3>Documentos Relacionados:</h3>
                  <ul>
                    {documents.map((doc, index) => (
                      <li key={index}>
                        <p><strong>ID:</strong> {doc.document_id}</p>
                        <p><strong>Fragmento:</strong> {doc.content_snippet}</p>
                        <p><strong>Similitud:</strong> {doc.similarity_score}</p>
                        <hr />
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

           {/* Botón para mostrar historial */}
           <button onClick={handleShowHistory}>Mostrar Historial</button>

              {showHistory && (
                <div className="history">
                  <h3>Historial de Chat:</h3>
                  <ul>
                    {chatHistory.map((msg, index) => (
                      <li key={index}>
                        <p><strong>Rol:</strong> {msg.role}</p>
                        <p><strong>Mensaje:</strong> {msg.content}</p>
                        <hr />
                      </li>
                    ))}
                  </ul>
                </div>
              )}
          
        </div>
      </header>
    </div>
  );
}

export default App;
