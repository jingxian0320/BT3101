## BT3101: Talking Data Dataset
## Author: Liu Yue
## Date: 29/09/2016 - 01/10/2016
## XAMPP Version: 3.2.1; MySQL Version: 5.6.21

## ETL Script: 	load data -> .csv files into database
##				transform data -> filter data
##				export data -> phone_brand, device_model, count as .csv file

## This script is to clean data to ensure each device is with recorded and labeled app events
## List of device_model is obtained in output file S0_device_model_count.csv
## List of brands is is obtained in output file S0_tk_phone_brand.csv


#### ETL Script:load data and remove duplicates ####
CREATE DATABASE tk_kaggle;
USE tk_kaggle;

## load events into the database ks_kaggle
CREATE TABLE events (
  event_id INT NOT NULL,
  device_id BIGINT,
  timestamp DATETIME,
  longitude NUMERIC(5, 2),
  latitude NUMERIC(5, 2),
  PRIMARY KEY(event_id)
);
LOAD DATA INFILE 'events.csv' INTO TABLE events FIELDS TERMINATED BY ',';
DELETE FROM events WHERE event_id = 0;
ALTER TABLE events DROP longitude;
ALTER TABLE events DROP latitude;
SELECT count(*) FROM events; ##3,252,950

## load app_labels into the database ks_kaggle
CREATE TABLE app_labels (
  app_id BIGINT NOT NULL,
  label_id INT NOT NULL
);
LOAD DATA INFILE 'app_labels.csv' INTO TABLE app_labels FIELDS TERMINATED BY ',';
DELETE FROM app_labels WHERE app_id = 0 AND label_id = 0;
ALTER IGNORE TABLE app_labels ADD UNIQUE INDEX app_with_label (app_id, label_id);
ALTER TABLE app_labels ADD CONSTRAINT app_with_label PRIMARY KEY (app_id, label_id);
SELECT count(*) FROM app_labels; ##459,452

## load app_events into the database ks_kaggle
CREATE TABLE app_events (
  event_id INT,
  app_id BIGINT,
  is_installed TINYINT,
  is_active TINYINT
);
LOAD DATA INFILE 'app_events.csv' INTO TABLE app_events FIELDS TERMINATED BY ',';
ALTER TABLE app_events ADD CONSTRAINT app_event_id PRIMARY KEY (event_id, app_id);
DELETE FROM app_events WHERE app_events.event_id = 0 AND app_events.app_id = 0;
SELECT count(*) FROM events; ##32,473,067

## load phone_brand_device_model into the database ks_kaggle
CREATE TABLE phone_brand_device_model (
  device_id BIGINT NOT NULL,
  phone_brand VARCHAR(100),
  device_model VARCHAR(100)
);
LOAD DATA INFILE 'phone_brand_device_model.csv' INTO TABLE phone_brand_device_model FIELDS TERMINATED BY ',';
DELETE FROM phone_brand_device_model WHERE device_id = 0;
ALTER IGNORE TABLE phone_brand_device_model ADD UNIQUE(device_id);
ALTER TABLE phone_brand_device_model ADD PRIMARY KEY(device_id);
SELECT count(*) FROM phone_brand_device_model; ##186,716




#### ETL Script: transform data with creating new tables ####

## Filter app_events to make sure each app belong to come categories
## Via deleteing app events with unrecorded app_lables
DELETE FROM app_events WHERE app_id NOT IN (SELECT DISTINCT app_id FROM app_labels);
SELECT count(*) FROM events; ##32,473,067

## Filter events to make sure each phone event is with recorded app event(s)
## Via finding phone events indexes with recorded app events & getting related attributs 
CREATE TABLE unique_event_id_app_events (
  event_id INT
);
INSERT INTO unique_event_id_app_events SELECT event_id FROM app_events;
ALTER IGNORE TABLE unique_event_id_app_events ADD UNIQUE(event_id);
CREATE TABLE events_w_app_events
  SELECT events.*
  FROM events
  INNER JOIN unique_event_id_app_events
  ON unique_event_id_app_events.event_id= events.event_id;
DROP TABLE unique_event_id_app_events;
ALTER TABLE events_w_app_events ADD PRIMARY KEY(event_id);
SELECT count(*) FROM events_w_app_events ; ##1,488,096

## Filter events to make sure each (phone event with app events) is with a recorded device model
## Via finding phone events indexes with recorded device model & getting related attributs 
CREATE TABLE events_final
  SELECT events_w_app_events.* FROM events_w_app_events
  WHERE device_id in (SELECT device_id FROM phone_brand_device_model);
SELECT count(*) FROM events_final; ## 1,446,145

## Filter phone_brand_device_model to make sure each device is with recorded app events 
## Via finding device_id indexes with (phone events with app events)& getting related attributs 
CREATE TABLE phone_brand_device_model_final
  SELECT phone_brand_device_model.*
  FROM phone_brand_device_model
  WHERE device_id IN (SELECT DISTINCT device_id FROM events_w_app_events);
ALTER TABLE phone_brand_device_model_final ADD PRIMARY KEY(device_id);
SELECT count(*) FROM phone_brand_device_model_final; ##58,462

## Count number of devices with (phone events with app events) under each device model
CREATE TABLE  device_model_count (
  model_id int NOT NULL AUTO_INCREMENT,
  phone_brand VARCHAR(100) NOT NULL ,
  device_model VARCHAR(100) NOT NULL,
  count INT,
  PRIMARY KEY (model_id)
);
INSERT INTO  device_model_count(phone_brand, device_model, count)
  SELECT phone_brand, device_model, COUNT(*) AS 'count'
  FROM phone_brand_device_model_final
  GROUP BY phone_brand, device_model;
SELECT count(*) FROM  device_model_count; #1217




#### ETL Script: export phone_brand, device_model, count as .csv file ####

## Export indexed list: phone_brand, device_model, count
SELECT * FROM  device_model_count
  INTO OUTFILE 'S0_device_model_count.csv'
  FIELDS ENCLOSED BY '"'
  TERMINATED BY ';'
  ESCAPED BY '"'
  LINES TERMINATED BY '\r\n';

## Export brand names having devices with (phone events with app events)
SELECT DISTINCT phone_brand FROM device_model_count
  INTO OUTFILE 'S0_tk_phone_brand.csv'
  FIELDS ENCLOSED BY '"'
  TERMINATED BY ';'
  ESCAPED BY '"'
  LINES TERMINATED BY '\r\n';
