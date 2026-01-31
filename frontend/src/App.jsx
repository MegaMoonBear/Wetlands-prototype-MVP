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

  // 
  const triggerFileUpload = () => {
  const fileInput = document.getElementById('photo-upload'); // Ensure the ID matches the input in index.html
  if (fileInput) {
    fileInput.click(); // Programmatically trigger the file input
  } else {
    console.error('File input not found');
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
    </>                                 {/* Closing React Fragment from Line 37 - find "return" section */}
  )
}

// Export the App component as the default export of this module to be used in other parts of the application
export default App 
