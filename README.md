# Wetlands Prototype MVP

## Index
1. [Introduction](#introduction)
2. [Backend Overview](#backend-overview)
3. [Frontend Overview](#frontend-overview)
4. [EXIF Metadata Extraction](#exif-metadata-extraction)
5. [Prompt options- Identifying Wetland Organisms](#PromptOptions---identifying-wetland-organisms)
6. [Lookup Tables vs ENUM](#lookup-tables-vs-enum)
7. [React Frontend Setup](#react-frontend-setup)
8. [How to Start the Frontend](#how-to-start-the-frontend)
9. [Recommended Photo Sites](#recommended-photo-sites)
10. [Diagnosing Performance Issues](#diagnosing-performance-issues)

---

## Introduction
This repository contains the Wetlands Prototype MVP, a project designed to analyze wetland images, extract metadata, and provide insights using AI models. The project includes a FastAPI backend, a React frontend, and PostgreSQL for data storage.

---

## Backend Overview
### Architecture
- **API Layer**: Handles HTTP requests and routes them to appropriate services.
- **Service Layer**: Contains business logic and interacts with the database and AI models.
- **Database**: Stores structured data for the application.
- **AI Model Integration**: Embeds AI models for inference tasks, such as image recognition and data analysis.

### Key Features
- **Frameworks**: Built using FastAPI for lightweight and efficient API handling.
- **Database**: Utilizes PostgreSQL for relational data storage.
- **AI Models**: Integrated using pre-trained models for specific tasks.
- **Environment Configuration**: Managed through `.env` files for secure and flexible deployment.

---

## Frontend Overview
### Key Features
- **Responsive Design**: Ensures compatibility across devices of various screen sizes.
- **React with Vite**: Provides a fast development environment and optimized builds.

---

## EXIF Metadata Extraction
### Why EXIF?
- **Widespread Support**: Embedded in most modern image formats (e.g., JPEG, TIFF).
- **Rich Metadata**: Includes date-time, camera settings, GPS coordinates, and more.
- **Ease of Use**: Libraries like Pillow make it straightforward to extract EXIF data.

### Limitations
- **Read-Only**: EXIF metadata is primarily read-only.
- **Not Universal**: Some images (e.g., screenshots) may lack EXIF metadata.

---

## Prompt options - Identifying Wetland Organisms
### Prompt Versions
1. **Multiple Choice**: Provides 1-3 possible identifications with a fact about the organism.
2. **Most Likely Identification**: Suggests the most likely organism visible in the image.
3. **Hidden Inhabitant**: Suggests an organism likely present but not visible based on habitat and metadata.

---

## Lookup Tables vs ENUM
### Why Lookup Tables?
- **Scalability**: Add new categories without schema changes.
- **Flexibility**: Supports regional variations and external GIS integration.
- **Analytics**: Easier to analyze evolving categories.

---

## React Frontend Setup
### Recommendations
- Start with JavaScript and React Compiler for simplicity and modern tooling.
- Transition to TypeScript in later phases if needed.

---

## How to Start the Frontend
1. **Install Dependencies**:
   ```bash
   npm install
   ```
2. **Start the Development Server**:
   ```bash
   npm start
   ```
3. **Open in Browser**:
   Navigate to the URL displayed in the terminal (e.g., `http://localhost:3000`).

---

## Recommended Photo Sites
- **Wolf River Greenway**: [Explore the Greenway](https://www.wolfriver.org/explore/greenway)
- **Wolf River Interactive Map**: [View Map](https://www.wolfriver.org/map)
- Bridges over culverts

---

## Diagnosing Performance Issues
### Common Issues
- High response times during large image uploads.
- Increased failure rates on metadata extraction endpoints.
- Fluctuating request rates causing slowdowns.

### Steps to Resolve
1. **Identify Log Patterns**:
   - Use Azure Monitor and Application Insights to analyze logs.
   - Example KQL Query:
     ```kql
     requests
     | where timestamp > ago(1h)
     | summarize count() by resultCode, bin(timestamp, 5m)
     ```
2. **Set Alerts**:
   - Define alert rules for high CPU usage, response times, and failure rates.
3. **Propose Corrective Actions**:
   - Short-term: Scale out resources.
   - Long-term: Optimize database queries and improve AI model efficiency.
