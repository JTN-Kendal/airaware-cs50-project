SELECT
    locations.name as loc_name,
    sub_locations.name as sub_name,
    pollutants.name as pollutant_name,
    value,
    status,
    measured_at
FROM measurements
JOIN sub_locations ON sub_locations.sub_location_id = measurements.sub_location_id
JOIN locations ON locations.location_id = sub_locations.location_id
JOIN pollutants ON pollutants.pollutant_id = measurements.pollutant_id
ORDER BY measured_at DESC
LIMIT 10
;

