import React, { useState } from 'react'
import './App.css'                    // CSS import same as Home or App for Contact page

// Moving the <script> section to a separate .js or .jsx file is a good practice for long-term design and maintainability. *Benefits of Moving to a Separate File*
  // Separation of Concerns: JavaScript logic in separate file ensures: 
      // HTML focuses solely on structure and content, while...
      // JavaScript handles behavior.
  // Reusability: Reapply across multiple HTML files or components
  // Readability and Maintainability: Easier managing and debugging code when HTML and JavaScript separate
  // Version Control: Changes easier to track in version control systems when logic in dedicated file
  // Scalability: Easier to scale and organize, especially as application grows in complexity
  // Performance: Browsers can cache external JavaScript files, improving load times on subsequent visits

// For Contact page, JavaScript to dynamically show/hide sections based on user input
function Contact() {
  // State to manage whether the contact method section is visible
  const [showContactMethod, setShowContactMethod] = useState(false);
  // State to store the selected contact method (e.g., email, text, call)
  const [contactMethod, setContactMethod] = useState('');
  // State to store the user's contact details (email or phone number)
  const [contactDetails, setContactDetails] = useState('');

  // Function to handle changes in the "Would you like a response?" dropdown
  const handleResponseChange = (event) => {
    if (event.target.value === 'yes') {
      setShowContactMethod(true); // Show the contact method section if "yes" is selected
    } else {
      setShowContactMethod(false); // Hide the contact method section if "no" is selected
      setContactMethod(''); // Clear the selected contact method
      setContactDetails(''); // Clear the contact details input
    }
  };

  // Function to handle changes in the contact method dropdown
  const handleContactMethodChange = (event) => {
    setContactMethod(event.target.value); // Update the selected contact method
    setContactDetails(''); // Clear the contact details input when the method changes
  };

  // Render the Contact form
  return (
    <div className="contact-form">
      <h1>Contact Us</h1>
      <form>
        {/* Dropdown to ask if the user wants a response */}
        <label htmlFor="response">Would you like a response?</label>
        <select id="response" onChange={handleResponseChange}>
          <option value="no">No</option>
          <option value="yes">Yes</option>
        </select>

        {/* Section to select the preferred contact method, shown only if "yes" is selected */}
        {showContactMethod && (
          <div id="contact-method-section">
            <label htmlFor="contact-method">Preferred Contact Method:</label>
            <select id="contact-method" value={contactMethod} onChange={handleContactMethodChange}>
              <option value="">Select a method</option>
              <option value="email">Email</option>
              <option value="text">Text</option>
              <option value="call">Call</option>
            </select>

            {/* Section to input contact details, shown only if a contact method is selected */}
            {contactMethod && (
              <div id="contact-details-section">
                <label htmlFor="contact-details">Contact Details:</label>
                <input
                  id="contact-details"
                  type={contactMethod === 'email' ? 'email' : 'tel'} // Input type changes based on the selected method
                  placeholder={
                    contactMethod === 'email'
                      ? 'Enter your email' // Placeholder for email input
                      : 'Enter your phone number' // Placeholder for phone input
                  }
                  value={contactDetails} // Controlled input value
                  onChange={(e) => setContactDetails(e.target.value)} // Update state on input change
                />
              </div>
            )}
          </div>
        )}

        {/* Submit button for the form */}
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default Contact;