import { useState } from 'react'
import './App.css'

// Functional component definition for the main App 
function App() {
  const [count, setCount] = useState(0) // State variable 'count' initialized to 0

  // Function to redirect to thanks.html page from home page's "Done..." section's "...1 min." buttons in index.html 
  const redirectToThanks = () => {
    window.location.href = '/thanks.html'; // redirect to thanks.html, when either "...1 min." button is clicked
  }

  // Function to fetch a fact about a previously uploaded photo from backend API from "Wait for description" button in index.html
  const fetchFact = async () => {
  try {
    const response = await fetch('/api/get-photo-fact'); // Replace with your API endpoint
    const data = await response.json();
    console.log(data.fact); // Log or display the fetched fact
  } catch (error) {
    console.error('Error fetching fact:', error);
  }
  };

  // This function triggers file input when "upload" button is clicked (not handling actual upload process - see next function).
  const triggerFileUpload = () => {
  const fileInput = document.getElementById('photo-upload'); // Ensure the ID matches the input in index.html
  if (fileInput) {
    fileInput.click(); // Programmatically trigger the file input
  } else {
    console.error('File input not found');
  }
  };

  // Function to send selected file to /api/images endpoint using a POST request, including a description.
    // Handles the file upload process by sending the file and metadata to the backend API at /api/images.  
  const uploadFile = async () => {
    const fileInput = document.getElementById('photo-upload'); // Get the file input element
    if (!fileInput || !fileInput.files.length) {
      console.error('No file selected');
      return;
    }

    const file = fileInput.files[0]; // Get the selected file
    const formData = new FormData();
    formData.append('file', file);
    formData.append('description', 'Uploaded via frontend'); // Add a description

    try {
      const response = await fetch('/api/images', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        console.log('File uploaded successfully:', data);
      } else {
        console.error('Failed to upload file:', response.statusText);
      }
    } catch (error) {
      console.error('Error during file upload:', error);
    }
  };

  // JSX return statement defining the UI structure for two buttons in index.html's "Done..." section
  return (                                        // JSX structure for the App component of the Vite + React app
    <>                        {/* React Fragment to group multiple elements without adding extra nodes to the DOM */}  
      <div>
        <h1>Vite + React</h1>                     {/* Main heading of the app */}

        <div className="card">                    {/* Card section with interactive button */}
          <button onClick={() => setCount((count) => count + 1)}>         {/* Button to increment count of clicks */}
            count is {count}
          </button>
        </div>

        
      </div>                                  
      {/* 2 "Done..." buttons in index.html's "Done..." section */}
      <button onClick={redirectToThanks}>Less than or at 1 min.</button>    {/* redirect to Thanks.html */}
      <button onClick={redirectToThanks}>More than 1 min.</button>          {/* redirect to Thanks.html */}
      <button onClick={fetchFact}>Wait for description</button> {/* Display database fact (next line) in index.html */}
                {/* While waiting... Another user's photo included a cattail, which are common wetland plants. */}
      <button onClick={triggerFileUpload}>Submit Another Photo</button> {/* Trigger file "upload" in index.html */} 
      <button onClick={uploadFile}>Submit Another Photo</button> {/* Upload the file to the /api/images endpoint */} 
    </>
  )                                                   
// Prior symbols close return JSX structure of "App" component and React Fragment from Lines 37-38 - find "return" section                                
}
// End of App component definition from Line 5

// Export the App component as the default export of this module to be used in other parts of the application
export default App
