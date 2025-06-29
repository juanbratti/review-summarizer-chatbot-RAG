import React, { useState } from "react";
import axios from "axios";
import "./FileUpload.css";

const FileUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState("");

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      const allowedTypes = ["text/plain", "text/csv", "application/csv"];
      const fileExtension = selectedFile.name.split(".").pop().toLowerCase();
      
      if (allowedTypes.includes(selectedFile.type) || ["txt", "csv"].includes(fileExtension)) {
        setFile(selectedFile);
        setUploadStatus("");
      } else {
        setUploadStatus("Por favor, selecciona un archivo .txt o .csv");
        setFile(null);
      }
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setUploadStatus("Por favor, selecciona un archivo primero");
      return;
    }

    setUploading(true);
    setUploadStatus("Subiendo archivo...");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const apiUrl = process.env.REACT_APP_API_URL || "http://localhost:8000";
      const response = await axios.post(`${apiUrl}/app/upload/`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setUploadStatus("¡Archivo subido exitosamente! Ya puedes hacer preguntas.");
      setFile(null);
      
      const fileInput = document.getElementById("file-upload");
      if (fileInput) fileInput.value = "";

      if (onUploadSuccess) {
        onUploadSuccess(response.data);
      }

    } catch (error) {
      console.error("Error uploading file:", error);
      
      let errorMessage = "Error al subir el archivo. ";
      if (error.response?.data?.detail) {
        errorMessage += error.response.data.detail;
      } else if (error.message) {
        errorMessage += error.message;
      } else {
        errorMessage += "Por favor, inténtalo de nuevo.";
      }
      
      setUploadStatus(errorMessage);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="file-upload-container">
      <div className="upload-section">
        <h3>📄 Subir Archivo de Reseñas</h3>
        <p>Sube un archivo .txt o .csv con reseñas de productos para empezar a hacer preguntas.</p>
        
        <div className="file-drop-zone">
          <input
            id="file-upload"
            type="file"
            accept=".txt,.csv"
            onChange={handleFileChange}
            disabled={uploading}
            className="file-input"
          />
          
          <div className="drop-zone-content">
            <div className="upload-icon">📁</div>
            <p>
              {file ? (
                <span className="file-selected">
                  <strong>Archivo seleccionado:</strong> {file.name}
                </span>
              ) : (
                <>
                  Arrastra un archivo aquí o <label htmlFor="file-upload" className="file-label">selecciona uno</label>
                </>
              )}
            </p>
            <small>Archivos soportados: .txt, .csv (máx. 10MB)</small>
          </div>
        </div>

        <button 
          onClick={handleUpload}
          disabled={!file || uploading}
          className={`upload-button ${!file || uploading ? "disabled" : ""}`}
        >
          {uploading ? (
            <>
              <span className="spinner"></span>
              Subiendo...
            </>
          ) : (
            "📤 Subir Archivo"
          )}
        </button>

        {uploadStatus && (
          <div className={`upload-status ${uploadStatus.includes("exitosamente") ? "success" : "error"}`}>
            {uploadStatus}
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUpload;
