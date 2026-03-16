<!-- Summary of PY files: db_utils, mokdels, and routes -->

### File Explanations:

#### 1. **`db_utils.py` (EXIF)**
   - Handles database interactions specifically for EXIF metadata.
   - Provides utility functions to insert, update, or query EXIF metadata in the database.
   - Ensures data integrity and proper handling of EXIF-related database operations.
   - Abstracts database logic to keep routes clean and focused on request handling.

#### 2. **models.py**
   - Defines the database schema and models for the application.
   - Contains functions for interacting with the database, such as fetching or inserting data.
   - Manages database connections and queries, ensuring efficient and secure data handling.
   - Acts as the central layer for database operations, used by other modules like `db_utils`.

#### 3. **routes.py (temp, ollama, perm as `/upload`)**
   - Defines API endpoints for the backend, including the `/upload-image` route.
   - Handles temporary file storage for uploaded images using `tempfile`.
   - Integrates AI analysis (e.g., Ollama Vision) to process uploaded images.
   - Manages permanent storage of files in the `uploads/` directory after processing.
   - Includes error handling for file uploads, AI processing, and database interactions.

---

### How They Work Together:

1. **File Upload and Temporary Storage**:
   - routes.py handles the `/upload-image` endpoint, saving uploaded files temporarily using `tempfile`.

2. **EXIF Metadata Extraction and Database Insertion**:
   - routes.py calls `db_utils.py` to insert extracted EXIF metadata into the database.
   - `db_utils.py` uses functions from `models.py` to interact with the database.

3. **AI Analysis Integration**:
   - `routes.py` integrates AI analysis (e.g., Ollama Vision) to process the uploaded image.
   - The results of the analysis are combined with EXIF metadata for further use.

4. **Permanent File Storage**:
   - After processing, routes.py moves the file to the `uploads/` directory for permanent storage.

5. **Centralized Database Management**:
   - models.py ensures all database interactions (from `db_utils.py` and `routes.py`) follow a consistent schema and logic.


**Key Components & Responsibilities**

see image with table of File, Primary Role, and Key Keywords/Functions

**Integration Workflow**

Ingestion: routes.py accepts the request and caches it in a temporary directory.

Intelligence: AI analysis (Ollama) is performed on the image content.

Extraction: Metadata is handed off to db_utils.py for processing.

Persistence: db_utils.py leverages models.py to write to the database, while routes.py moves the physical file to permanent storage.

**Key Function Interactions**

Temporary Hand-off: routes.py manages the lifecycle of the file. It ensures the file exists in tempfile long enough for both AI analysis and EXIF extraction before moving it to uploads/.

Layered DB Access: routes.py never talks to the database directly. It passes high-level data to db_utils.py, which then maps that data to the specific CRUD operations defined in models.py.

Error Boundaries: If the AI analysis or EXIF extraction fails, routes.py is responsible for cleaning up the tempfile and returning the appropriate error code to the Client.