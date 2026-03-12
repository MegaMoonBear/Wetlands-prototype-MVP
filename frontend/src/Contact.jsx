import React, { useState } from 'react'
import './App.css'                    // CSS import same as Home or App for Contact page

// src/pages/Contact.jsx
import { useState } from "react";

export default function Contact({ onSubmitFeedback }) {
  const [topic, setTopic] = useState("");
  const [details, setDetails] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    onSubmitFeedback({ topic, details });
    setTopic("");
    setDetails("");
  }

  return (
    <div style={styles.wrapper}>
      <h2>Contact / Feedback</h2>

      <form onSubmit={handleSubmit} style={styles.form}>
        {/* <label>
          Topic:
          <select
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            required
          >
            <option value="">Select a Topic:</option>
            <option value="technical">Technical Issue</option> 
            <option value="feedback">Constructive Feedback</option> 
            <option value="positive">Positive Feedback</option> 
            <option value="mixed">Mixed Feedback</option> 
            <option value="other">Other (Please specify in "Details")</option> 
          </select>
        </label> */}

        <select name="" id="">
           <option value="">Select a Topic:</option>
        </select>

        <label>
          Details:
          <textarea
            value={details}
            onChange={(e) => setDetails(e.target.value)}
            placeholder="Describe your issue or suggestion..."
            rows={5}
            required
          />
        </label>

        <button type="submit">Submit</button>
      </form>
    </div>
  );
}


export default Contact;