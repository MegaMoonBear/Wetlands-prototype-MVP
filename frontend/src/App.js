// import logo from './assets/WaterSnapMap_Logo_ChatGPT.png'; -- IGNORE, since... 
    // "For React components, you cannot use import for files in the public folder" ---

// import React from 'react';
import './App.css';

// The App function is a React functional component that:
  // Renders the main structure of the app,...
    // inclu.: header with logo, some instructional text, and link to React docum.
  // Uses JSX to define the layout and dynamically include the logo image.
function App() {
  // Define the path to the logo stored in the public folder
  const logoPath = "/WaterSnapMap_Logo_ChatGPT.png";

  return (
    <div className="App">
      <header className="App-header">
        {/* Render the logo using the defined path */}
        <img src={logoPath} alt="Logo" className="App-logo" />

        {/* Instructional text for editing the file */}
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>

        {/* Link to the React documentation */}
        <a className="App-link" href="https://reactjs.org" target="_blank" rel="noopener noreferrer"> 
          Learn React 
        </a>
      </header>
    </div>
  );
}

export default App;
