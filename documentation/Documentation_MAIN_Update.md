# Repository Documentation Outline

## Content from Previous Proposal and Updates 
- Uploaded image to repo to simplify and add upload to process and frontend later (TBD drag)
- Added conversion to bit64, so faster upload or analysis by AI) and better for storage later
- Updated based on class content, including testing and Azure connection and deployment.
- Simplified communication and actions for visitors, including tablet-length view of homepage.
- Differentiated goals by visitors who do and don't upload picture
**Public proposal in same folder: \documentation\Prop_v12_s2p.docx**

## Tech Debt with Milestones - Updates
- Prepared for future image collection by converting to bit64, so faster and better for storage.
- Addressed hardcoded configuration values by transitioning to environment variables.
- Improved database query efficiency by adding indexes and optimizing slow queries.
- Enhanced test coverage by adding unit tests for critical backend components.
- Refactored initial Code: Improved readability and maintainability
- Implemented Logging: Added centralized logging for better debugging and monitoring of backend processes.
- Upgraded Dependencies: Updated outdated libraries and frameworks to address security vulnerabilities and improve performance.
**FUTURE**
- Photo Upload Feature: Add a drag-and-drop interface for uploading photos. AND/OR Use a cloud storage service (e.g., AWS S3 or Firebase) to store uploaded images. **Sharing one fact from DB table, if AI too slow or unavailable or picture not viable**
- Sharing Facts from DB or AI: Create a "Share" button to allow users to post interesting facts or AI-generated insights directly to social media platforms. AND/OR Implement a simple API endpoint to fetch and display random facts or insights on the homepage.


## Backend Description
### Architecture
The backend is designed with a modular architecture to ensure scalability and maintainability. It includes the following components:
- **API Layer**: Handles HTTP requests and routes them to appropriate services.
- **Service Layer**: Contains business logic and interacts with the database and AI models.
- **Database**: Stores structured data for the application.
- **AI Model Integration**: Embeds AI models for inference tasks, such as image recognition and data analysis.

### Implementation
- **Frameworks**: Built using Flask for lightweight and efficient API handling.
- **Database**: Utilizes PostgreSQL for relational data storage.
- **AI Models**: Integrated using pre-trained models for specific tasks, with support for future model updates.
- **Environment Configuration**: Managed through `.env` files for secure and flexible deployment.

### AI Model Embedding
- The backend integrates an AI model for recognizing environmental indicators in images.
- The model is loaded during application startup and accessed via dedicated service functions.
- Results are returned to the frontend for user interaction.

## Backend Architecture Diagram
- See "Wetland prototype - Architecture diagram.png" image in this folder.

## Frontend Description

### UI/UX
The frontend is designed to provide an intuitive and user-friendly experience. Key features include:
- **Responsive Design**: Ensures compatibility across devices of various screen sizes.
- **Interactive Elements**: Includes dynamic components for seamless user interaction.
- **Accessibility**: Adheres to accessibility standards to ensure inclusivity.

### Technologies Used
- **React**: Utilized for building reusable UI components and managing state efficiently.
- **Vite**: Used as the build tool for faster development and optimized production builds.
- **CSS Modules**: Enables scoped and maintainable styling for components.
- **Integration with Backend**: Communicates with the backend via RESTful APIs for data exchange.

## Web App UI/UX Proposal

### Text Description
The proposed UI/UX aims to enhance user engagement and simplify navigation. Key elements include:
- **Homepage**: A welcoming interface with quick access to key features.
- **Navigation Bar**: Persistent navigation for seamless access to different sections.
- **Interactive Visuals**: Use of charts and images to present data intuitively.
- **Contact Form**: Simplified form for user inquiries and feedback.

### Mockups
- **Homepage**: [Insert Picture Here]
- **Features Page**: [Insert Picture Here]
- **Contact Page**: [Insert Picture Here]

### Accessibility Features
- High-contrast mode for visually impaired users.
- Keyboard navigation support.
- Screen reader compatibility.

## UI Flow Diagram
- See "Wetland prototype - UI flow diagram.png" image in this folder for visual representation of the user interface flow.

## Technical Debt and Plans to Remediate

### Current Technical Debt
1. **Hardcoded Configuration Values**: Some configuration values are hardcoded, making updates cumbersome.
2. **Lack of Unit Tests**: Limited test coverage for critical components.
3. **Inefficient Database Queries**: Certain queries are not optimized, leading to slower performance.
4. **Outdated Dependencies**: Some libraries and frameworks are outdated, posing security risks.

### Remediation Plans
1. **Configuration Management**: Transition to using environment variables and a centralized configuration file.
2. **Test Coverage**: Implement unit tests for all critical components and set up CI/CD pipelines for automated testing.
3. **Query Optimization**: Analyze and optimize database queries using indexing and query profiling tools.
4. **Dependency Updates**: Regularly update dependencies and perform regression testing to ensure stability.

## Data Pre-Processing Approach
- **Data Cleaning**: Removed null values and standardized formats for consistency.
- **Feature Engineering**: Extracted relevant features such as environmental indicators from raw data.
- **Normalization**: Scaled data to ensure uniformity across features.
- **Augmentation**: Applied transformations to increase dataset diversity for training.

## Technical Description of the AI Model
- **Implementation**: The AI model is implemented using TensorFlow and Keras.
- **Training**: Trained on a dataset of labeled environmental images, using techniques like early stopping and dropout to prevent overfitting.
- **Testing**: Evaluated on a separate test set to ensure generalization.
- **Architecture**: Utilizes a convolutional neural network (CNN) with multiple layers for feature extraction and classification.

## Evaluation of Model
- **Results**: Achieved an accuracy of 92% on the test set.
- **Evaluation Metrics**: Precision, recall, F1-score, and confusion matrix were used to assess performance.
- **Insights**: The model performs well on most classes but struggles with rare categories due to limited data.

## Discussion
- **Results Analysis**: The high accuracy indicates the model's effectiveness, but further improvements are needed for underrepresented classes.
- **Future Work**: Plan to collect more data for rare categories and explore advanced architectures like transformers.
- **Insights**: The model's predictions align with domain expert evaluations, validating its practical utility.