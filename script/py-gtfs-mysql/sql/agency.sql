CREATE TABLE `agency` (
    agency_id VARCHAR(11) PRIMARY KEY,
    agency_name VARCHAR(255),
    agency_url VARCHAR(255),
    agency_timezone VARCHAR(50),
    agency_lang VARCHAR(3),
    agency_phone VARCHAR(50),
    agency_fare_url VARCHAR(255)
);