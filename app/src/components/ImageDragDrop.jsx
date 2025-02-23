import React, { useState } from "react";

function ImageDragDrop() {
  const [imagePath, setImagePath] = useState(null); // Blob URL (laikinas kelias)
  const [fileName, setFileName] = useState(null); // Failo pavadinimas
  const [fileType, setFileType] = useState(null); // Failo tipas
  const [selectedFile, setSelectedFile] = useState(null); // Tikras failo objektas

  const handleDrop = (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];

    if (file && file.type.startsWith("image/")) {
      setSelectedFile(file); // Išsaugome failą objektą
      setImagePath(URL.createObjectURL(file)); // Sukuriame peržiūros URL
      setFileName(file.name); // Išsaugome tikrą failo pavadinimą
      setFileType(file.type); // Išsaugome failo tipą (MIME type)
    } else {
      alert("Prašome įkelti tik paveikslėlius");
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  return (
    <div
      className="container"
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        width: "100vw",
      }}
    >
      <div
        className="drag-drop-wrapper"
        style={{
          display: "flex",
          flexDirection: "row",
          alignItems: "center",
          justifyContent: "center",
          width: "80%",
          maxWidth: "800px",
          border: "2px solid #ddd",
          borderRadius: "10px",
          padding: "20px",
          background: "#f9f9f9",
          boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.1)",
        }}
      >
        {/* Drag and Drop zona */}
        <div
          className="drag-drop-area"
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          style={{
            width: "50%",
            height: "300px",
            border: "2px dashed #ccc",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexDirection: "column",
            position: "relative",
            overflow: "hidden",
            textAlign: "center",
            borderRadius: "8px",
            background: "#fff",
          }}
        >
          <p>Įkelkite nuotrauką</p>
          {imagePath && (
            <img
              src={imagePath}
              alt="Preview"
              style={{
                maxWidth: "90%",
                maxHeight: "90%",
                objectFit: "contain",
                position: "absolute",
              }}
            />
          )}
        </div>

        {/* Informacijos zona */}
        <div
          className="image-info"
          style={{
            width: "50%",
            padding: "20px",
            textAlign: "left",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <h2>Failo informacija:</h2>

          {fileName ? (
            <>
              <p><strong>Failo pavadinimas:</strong> {fileName}</p>
              <p><strong>Failo tipas:</strong> {fileType}</p>
              <p><strong>Failo kelias:</strong> {imagePath}</p>
            </>
          ) : (
            <p>Pasirinkite nuotrauką, kad pamatytumėte informaciją.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default ImageDragDrop;