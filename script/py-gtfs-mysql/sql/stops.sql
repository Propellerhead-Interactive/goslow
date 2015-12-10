CREATE TABLE `stops` (
    stop_id VARCHAR(15) PRIMARY KEY,
    stop_code VARCHAR(50),
	stop_name VARCHAR(255),
	stop_desc VARCHAR(255),
	stop_lat VARCHAR(20),
	stop_lon VARCHAR(20),
	zone_id VARCHAR(11),
	stop_url VARCHAR(255),
	location_type INT(2),
	parent_station VARCHAR(15),
	stop_timezone VARCHAR(255),
	wheelchair_boarding INT(1),
	KEY `zone_id` (zone_id),
	KEY `stop_lat` (stop_lat),
	KEY `stop_lon` (stop_lon),
	KEY `location_type` (location_type),
	KEY `parent_station` (parent_station)
);