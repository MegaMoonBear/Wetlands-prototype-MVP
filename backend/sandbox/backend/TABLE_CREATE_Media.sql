-- Connect to PGSQL and create the submissions table
-- This SQL script creates a table to store user's photo submissions with 
    -- UUIDs, timestamps, text fields

-- PostgreSQL command: turns on built‑in plugin - database needs to generate UUIDs inside SQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp"; -- Enable UUID generation extension

-- Create the media table for users' submissions 
    -- ML-ready asset management
    -- Why sponsors care
        -- Reusable training data for future AI initiatives
        -- Demonstrates forward-looking technical vision
        -- Supports communications and storytelling
    -- Why data requestors want it
        -- Enables model retraining and validation
        -- Preserves raw evidence for re-analysis
        -- Supports quality assurance workflows
CREATE TABLE submissions (
    id media_UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_ID TEXT,
    media_type ENUM('image', 'video', 'audio') NOT NULL,
    metadata_extracted boolean DEFAULT FALSE, -- Y/N - flag for metadata extraction
    storage_url TEXT, -- URL/path to media stored in cloud 
    tags_user_device TEXT[], -- Tags from user/device 
    -- TEXT[] as array datatype (text)
    tags_AI_Option1 TEXT, -- Tags from AI option 1
    tags_AI_Option2 TEXT, -- Tags from AI option 2
    tags_AI_Option3 TEXT, -- Tags from AI option 3
    tag_user_Selected1 TEXT -- Tag selected by user in app - only 1
    tag_user_Selected1_ConfidL ENUM -- Confidence level for 1 user-selected tag
);
