-- Create database if not exists
CREATE DATABASE IF NOT EXISTS country_currency_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE country_currency_db;

-- Drop table if exists (for clean setup)
DROP TABLE IF EXISTS countries;

-- Create countries table
CREATE TABLE countries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    capital VARCHAR(255),
    region VARCHAR(100),
    population BIGINT NOT NULL,
    currency_code VARCHAR(10),
    exchange_rate DECIMAL(15, 6),
    estimated_gdp DECIMAL(20, 2),
    flag_url TEXT,
    last_refreshed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_name (name),
    INDEX idx_region (region),
    INDEX idx_currency (currency_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create metadata table for tracking refresh timestamps
DROP TABLE IF EXISTS refresh_metadata;

CREATE TABLE refresh_metadata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    last_refreshed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert initial metadata record
INSERT INTO refresh_metadata (id) VALUES (1);