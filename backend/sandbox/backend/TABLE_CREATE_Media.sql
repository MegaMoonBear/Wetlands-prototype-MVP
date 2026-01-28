-- Connect to PGSQL and create the observations table
-- This SQL script creates a table to store user's photo observations with 
    -- UUIDs, timestamps, text fields

-- PostgreSQL command: turns on built‑in plugin - database needs to generate UUIDs inside SQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp"; -- Enable UUID generation extension

-- Create the observations table with soft delete functionality
CREATE TABLE observations (
    id observation_UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    observed_at TIMESTAMP WITH TIME ZONE, -- Date-time of observation
    data_source ENUM('user_upload', 'sensor', 'third_party') NOT NULL, -- Source of observation/photo
    user_UUID TEXT,
    tags_user_device TEXT[], -- Tags from user/device 
    tags_AI_ConfidL ENUM, -- Confidence level for primary/first AI-suggested tag
    tags_AI_Option1 TEXT, -- Tags from AI option 1
    tags_AI_Option2 TEXT, -- Tags from AI option 2
    tags_AI_Option3 TEXT, -- Tags from AI option 3
    tag_user_Selected1 TEXT, -- Tag selected by user in app - only 1
    tag_user_Selected1_ConfidL ENUM, -- Confidence level for 1 user-selected tag
    validation_status ENUM('pending', 'validated', 'rejected') DEFAULT 'pending', 
    -- V-status for user-selected tag
    validation_reject ENUM('updated', 'awaiting expert review', 'unidentifiable') DEFAULT 'awaiting expert review',
    is_deleted BOOLEAN DEFAULT FALSE -- Soft delete flag to mark rows as deleted
);

-- Add an index to optimize queries filtering by is_deleted
CREATE INDEX idx_observations_is_deleted ON observations (is_deleted); -- helps performance with soft delete 

-- OTHER database's tables 
-- media table for observation_ID, media_ID, metadata_extracted, and storage_URL; and 
CREATE TABLE media (
    id media_UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    observation_UUID UUID REFERENCES observations(id), -- Soft delete reference
    media_type ENUM('image', 'video', 'audio') NOT NULL, -- 
    metadata_extracted boolean DEFAULT FALSE, -- Y/N - flag for metadata extraction
    storage_url TEXT -- URL/path to media stored... in CLOUD or CACHE? 
);

-- Table to store EXIF metadata extracted from media files
CREATE TABLE pic_metadata_exif (
    id SERIAL PRIMARY KEY,
    media_id UUID REFERENCES media(id) ON DELETE CASCADE, -- Link to media table
    camera_make TEXT, -- Camera manufacturer
    camera_model TEXT, -- Camera model
    datetime_original TIMESTAMP, -- Original date and time of capture
    -- Latitude and longitude are derived from EXIF GPS data but should align with the location table
    altitude DOUBLE PRECISION, -- Altitude from EXIF GPS data
    orientation TEXT, -- Orientation of the image
    exposure_time TEXT, -- Exposure time (e.g., "1/200")
    f_number TEXT, -- Aperture value (e.g., "f/2.8")
    iso INTEGER, -- ISO speed
    focal_length TEXT, -- Focal length (e.g., "50mm")
    flash TEXT, -- Flash information (e.g., "Fired")
    additional_metadata JSONB -- Store any additional EXIF data as JSON
);

CREATE TABLE indicator_decompObs (
    id indicator_UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    observation_UUID UUID REFERENCES observations(id), -- Soft delete reference
    user_ID UUID REFERENCES Roles_Governance(id), -- FK to track user submitting or validating
    indicator_type ENUM('water', 'plant', 'animal', 'unknown'), -- Type of indicator of water flow or ecosystem health
    indicator_name TEXT, -- e.g., 'species_presence', 'water_flow', etc.
    severity_level ENUM('low', 'medium', 'high', 'unknown') -- Severity or significance level for the indicator, for example: species rarity or water contamination    
);

CREATE TABLE Roles_Governance (
    id user_UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    observation_UUID UUID REFERENCES observations(id), -- Soft delete reference
    user_role ENUM('admin/developer', 'public', 'professional reviewer') -- Tracks governance roles for users
    cohort ENUM('internal_testers', 'pilot_users', 'public_launch') -- User cohort for phased roll-out
    consent_version ENUM('v1.0', 'v1.1', 'v2.0') -- Tracks legal consent version agreed to by user
);

-- mixes **scale**, **legal status**, and **use** into single ENUMs - hard to parse later
-- INITIAL location table with location_ID, latitude and longitude) for the metadata? 
-- Updated with improved schema below to: 
    -- Prevents **ENUM inflation* later
    -- Aligns with **standard GIS layers & zoning codes**
    -- Supports **wetland + conservation + civic planning use cases**
    -- Keeps the schema understandable for **non-technical users**
-- Updates will improve analytics with minimal complexity
CREATE TABLE location (
    id location_UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    observation_UUID UUID REFERENCES observations(id), -- Soft delete reference
    user_ID UUID REFERENCES Roles_Governance(id), -- FK to track user submitting or validating
    spatial_context ENUM(
        'site',            -- single parcel or point-of-interest
        'park_or_reserve', -- mapped greenspace
        'corridor',        -- trail, greenway, riparian buffer
        'neighborhood',
        'urban_core',      -- `urban` splits into urban/suburban/rural for better modeling
        'suburban',
        'rural',
        'agricultural_landscape'
    ), -- GIS-based, if not in metadata
    ownership_type ENUM(
        'public_federal',
        'public_state',
        'public_local',
        'tribal',
        'nonprofit',
        'private_individual',
        'private_corporate',
        'institutional',
        'unknown'
    ), -- from GIS overlay
    land_use_primary ENUM(
        'protected_conservation',
        'recreation',
        'residential',
        'commercial',
        'industrial',
        'institutional',
        'education',
        'agriculture_crops',
        'agriculture_livestock',
        'natural_unmanaged',
        'mixed_use'
    ), -- from GIS overlay or user
    known_wetland ENUM('wetland', 'floodplain', 'riparian_buffer', 'critical_habitat', 'none', 'unknown') DEFAULT 'unknown', -- Environmental designation
    public_access ENUM(
        'open_access',
        'limited_access',
        'permit_required',
        'restricted',
        'no_public_access'
    ), -- Access type for community use and equity mapping
    classification_source ENUM(
        'gis_overlay',
        'user_reported',
        'field_verified',
        'inferred',
        'unknown'
    ) -- Data provenance for quality assurance
);

/* =========================================================
   MAIN TABLE: Water observations (Phase 1)
   Purpose:
   - Capture AI- and user-observed ecological signals
   - Use one indicator species + visual water traits
   - Support early water quality inference without chemistry
   ========================================================= */

CREATE TABLE water_observation (
    id water_obs_UUID PRIMARY KEY,

    -- Spatial and contextual references
    location_id UUID NOT NULL,
    waterbody_type_id INT NOT NULL,
    spatial_context_id INT,

    -- Indicator species (Phase 1: single species)
    indicator_species_id INT NOT NULL,
    indicator_decompObs_id UUID REFERENCES indicator_decompObs(id), -- FK to connect with indicator_decompObs
    species_presence ENUM (
        'present',
        'absent',
        'uncertain'
    ) NOT NULL,
    -- Visually observable water characteristics (AI-derivable)
    flow_type ENUM (
        'still',
        'slow_moving',
        'fast_moving',
        'unknown'
    ),
    water_color ENUM (
        'clear',
        'brown',
        'green',
        'blue',
        'black',
        'other',
        'unknown'
    ),
    turbidity_level ENUM (
        'low',
        'moderate',
        'high',
        'unknown'
    ),
    surface_conditions SET (
        'foam',
        'oil_sheen',
        'algal_mat',
        'debris',
        'none_observed'
    ),
    -- AI / data provenance metadata
    ai_confidence_score DECIMAL(3,2),
    classification_source ENUM (
        'ai_image',
        'user_reported',
        'field_verified'
    ) NOT NULL,
    observed_at TIMESTAMP NOT NULL
);


/* ============  LOOKUP TABLES FOR ENUM REPLACEMENT (Phase 2) =================================== */
-- Remove ENUMs so they are fully replaced with "lookup tables" for... 
-- scalability and better integration with GIS layers, hydrology, and other references.


-- Lookup table for spatial_context
CREATE TABLE spatial_context_lookup (
    id SERIAL PRIMARY KEY,
    context_name TEXT UNIQUE NOT NULL, -- e.g., 'site', 'park_or_reserve', etc.
    description TEXT -- Optional description for the context
);

-- Lookup table for ownership_type
CREATE TABLE ownership_type_lookup (
    id SERIAL PRIMARY KEY,
    ownership_name TEXT UNIQUE NOT NULL, -- e.g., 'public_federal', 'private_individual', etc.
    description TEXT -- Optional description for the ownership type
);

-- Lookup table for land_use_primary
CREATE TABLE land_use_primary_lookup (
    id SERIAL PRIMARY KEY,
    use_name TEXT UNIQUE NOT NULL, -- e.g., 'protected_conservation', 'residential', etc.
    description TEXT -- Optional description for the land use
);

-- Lookup table for known_wetland
CREATE TABLE known_wetland_lookup (
    id SERIAL PRIMARY KEY,
    wetland_status TEXT UNIQUE NOT NULL, -- e.g., 'wetland', 'floodplain', etc.
    description TEXT -- Optional description for the wetland status
);

-- Lookup table for public_access
CREATE TABLE public_access_lookup (
    id SERIAL PRIMARY KEY,
    access_type TEXT UNIQUE NOT NULL, -- e.g., 'open_access', 'restricted', etc.
    description TEXT -- Optional description for the access type
);

-- Lookup table for classification_source
CREATE TABLE classification_source_lookup (
    id SERIAL PRIMARY KEY,
    source_name TEXT UNIQUE NOT NULL, -- e.g., 'gis_overlay', 'user_reported', etc.
    description TEXT -- Optional description for the classification source
);
-- These lookup tables will replace the ENUM fields in the main tables
-- during Phase 2 of the database schema update.
