-- Create table users
-- depends:

CREATE TABLE users (
	telegram_id INT PRIMARY KEY,
	username VARCHAR(255),
	height INT, -- рост в см
	weight INT, -- вес в кг
	age INT,
	physical_activity_level INT -- уровень физической активности 0...2
		CHECK (physical_activity_level >= 0 AND physical_activity_level <= 2) 
);

