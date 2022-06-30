CREATE DATABASE smart_building;

USE smart_building;

CREATE TABLE smart_building.thermostat(
    record  DATETIME PRIMARY KEY,
    floor_no INT NOT NULL,
    room_no INT NOT NULL,
    temp_level FLOAT(3,2) NOT NULL
);

CREATE TABLE smart_building.humidity(
    record  DATETIME PRIMARY KEY,
    floor_no INT NOT NULL,
    room_no INT NOT NULL,
    humidity_level FLOAT(3,2) NOT NULL
);

CREATE TABLE smart_building.boiler(
    record  DATETIME PRIMARY KEY,
    floor_no INT NOT NULL,
    room_no INT NOT NULL,
    active BOOL NOT NULL
);

CREATE TABLE smart_building.chiller(
    record  DATETIME PRIMARY KEY,
    floor_no INT NOT NULL,
    room_no INT NOT NULL,
    active BOOL NOT NULL
);

CREATE TABLE smart_building.ahu(
    record  DATETIME PRIMARY KEY,
    floor_no INT NOT NULL,
    room_no INT NOT NULL,
    fan_speed FLOAT(3,2) NOT NULL
);

CREATE TABLE smart_building.intensity(
    record  DATETIME PRIMARY KEY,
    floor_no INT NOT NULL,
    room_no INT NOT NULL,
    light_level INT NOT NULL
);

CREATE TABLE smart_building.light(
    record  DATETIME PRIMARY KEY,
    floor_no INT NOT NULL,
    room_no INT NOT NULL,
    active bool NOT NULL
);

CREATE TABLE smart_building.fire_detect(
    record  DATETIME PRIMARY KEY,
    floor_no INT NOT NULL,
    room_no INT NOT NULL,
    active bool NOT NULL
);

CREATE TABLE smart_building.smoke_detect(
    record  DATETIME PRIMARY KEY,
    floor_no INT NOT NULL,
    room_no INT NOT NULL,
    smoke_level INT NOT NULL
);


CREATE TABLE smart_building.sprinkler(
    record  DATETIME PRIMARY KEY,
    floor_no INT NOT NULL,
    room_no INT NOT NULL,
    active bool NOT NULL
);

CREATE TABLE smart_building.fire_alarm(
    record  DATETIME PRIMARY KEY,
    floor_no INT NOT NULL,
    room_no INT NOT NULL,
    active bool NOT NULL
);

CREATE TABLE smart_building.pull_alarm(
    record  DATETIME PRIMARY KEY,
    floor_no INT NOT NULL,
    room_no INT NOT NULL,
    active bool NOT NULL
);
