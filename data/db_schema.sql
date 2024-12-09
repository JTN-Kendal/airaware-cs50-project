-- Locations table to store main locations (Oxford, SODC Henley, etc.)
CREATE TABLE locations (
    location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Sub-locations table (High Street, St Aldates, etc.)
CREATE TABLE sub_locations (
    sub_location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    UNIQUE(location_id, name),
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

-- Pollutants table (simplified without unit)
CREATE TABLE pollutants (
    pollutant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Measurements table
CREATE TABLE measurements (
    measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sub_location_id INTEGER NOT NULL,
    pollutant_id INTEGER NOT NULL,
    value REAL NOT NULL,
    status TEXT NOT NULL,
    measured_at DATE NOT NULL,
    FOREIGN KEY (sub_location_id) REFERENCES sub_locations(sub_location_id),
    FOREIGN KEY (pollutant_id) REFERENCES pollutants(pollutant_id)
);

-- Create indices for common query patterns
CREATE INDEX idx_measurements_date ON measurements(measured_at);
CREATE INDEX idx_measurements_location ON measurements(sub_location_id);
CREATE INDEX idx_measurements_pollutant ON measurements(pollutant_id);