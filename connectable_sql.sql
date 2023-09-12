DROP SCHEMA IF EXISTS `connectable` ;

CREATE SCHEMA IF NOT EXISTS `connectable`;

USE `connectable` ;

DROP TABLE IF EXISTS `connectable`.`users` ;

CREATE TABLE IF NOT EXISTS `connectable`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `dob` DATE NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`));

DROP TABLE IF EXISTS `connectable`.`events` ;
CREATE TABLE IF NOT EXISTS `connectable`.`events` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `location` VARCHAR(45) NULL,
  `description` VARCHAR(255) NULL,
  `date_made` DATETIME NULL,
  `slots` INT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
);


DROP TABLE IF EXISTS `connectable`.`attendees` ;
CREATE TABLE IF NOT EXISTS `connectable`.`attendees` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `event_id` INT NOT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  FOREIGN KEY (`event_id`) REFERENCES `events` (`id`)
);