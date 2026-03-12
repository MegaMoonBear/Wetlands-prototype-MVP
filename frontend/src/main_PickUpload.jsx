// This file contains two components: Main and FilePicker.
// Main provides layout styling, while FilePicker handles file upload functionality.

import { useState } from "react";

// Main component: Defines the layout and structure for the application content.
export function Main({ children }) {
  return (
    <main style={mainStyles}>
      {children}
    </main>
  );
}

const mainStyles = {
  padding: "1.5rem",
  minHeight: "70vh",
};

// FilePicker component: Provides a user interface for selecting and uploading files.
export function FilePicker({ onUpload }) {
  const [file, setFile] = useState(null); // State to track the selected file

  const handleChoose = (e) => setFile(e.target.files[0]); // Updates state with the chosen file

  const handleUpload = () => {
    if (file) onUpload(file); // Calls the parent-provided upload function if a file is selected
  };

  return (
    <div style={filePickerStyles.wrapper}>
      <input type="file" onChange={handleChoose} /> {/* File input field */}
      <button onClick={handleUpload} disabled={!file}> {/* Upload button, disabled if no file */}
        Upload File
      </button>
    </div>
  );
}

const filePickerStyles = {
  wrapper: {
    display: "flex",
    gap: "1rem",
    alignItems: "center",
  },
};