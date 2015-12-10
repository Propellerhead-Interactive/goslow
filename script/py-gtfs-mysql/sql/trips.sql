CREATE TABLE `trips` (
    route_id VARCHAR(15),
	service_id VARCHAR(15),
	trip_id VARCHAR(20) PRIMARY KEY,
	trip_headsign VARCHAR(255),
	trip_short_name VARCHAR(255),
	direction_id TINYINT(1),
	block_id VARCHAR(15),
	shape_id VARCHAR(15),
	wheelchair_accessible INT(1),
	bikes_allowed INT(1),
	route_variant VARCHAR(5),
	KEY `route_id` (route_id),
	KEY `service_id` (service_id),
	KEY `direction_id` (direction_id),
	KEY `block_id` (block_id),
	KEY `shape_id` (shape_id)
);