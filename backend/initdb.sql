/* Creating a new Database */
DROP DATABASE IF EXISTS `heroku_14806ad62e1ed9f`;
CREATE DATABASE `heroku_14806ad62e1ed9f`;
USE `heroku_14806ad62e1ed9f`;

/* Creating SESSION_DATA Table */
DROP TABLE IF EXISTS `SESSION_DATA`;
CREATE TABLE `SESSION_DATA`(
    `SESSION_ID` INT AUTO_INCREMENT PRIMARY KEY,
    `SCENARIO` VARCHAR(1) NOT NULL,
    `TASK_SCENARIO` INT NOT NULL,
    `SOURCE` VARCHAR(1) NOT NULL,
    `OLD_PARTICIPANT` VARCHAR(1) NOT NULL,
    `FINISHED` VARCHAR(1) NOT NULL,
    `CREATED_AT` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

/* Creating CREATED_TASKS Table */
DROP TABLE IF EXISTS `CREATED_TASKS`;
CREATE TABLE `CREATED_TASKS`(
    `ID` INT AUTO_INCREMENT PRIMARY KEY,
    `SESSION_ID` INT REFERENCES SESSION_DATA(SESSION_ID),
    `TITLE` TEXT NOT NULL,
    `DESCRIPTION` TEXT NOT NULL,
    `CREATED_AT` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS `EVALUATION_DATA`;
CREATE TABLE `EVALUATION_DATA`(
    `ID` INT AUTO_INCREMENT PRIMARY KEY,
    `SESSION_ID` INT REFERENCES SESSION_DATA(SESSION_ID),
    `EXPERIENCE` INT NOT NULL,
    `PLATFORMS` TEXT NOT NULL,
    `MOST_USED_PLATFORM` VARCHAR(40) NOT NULL,
    `MOST_TASKS` INT NOT NULL,
    `Q1` VARCHAR(1) NOT NULL,
    `Q2` VARCHAR(1) NOT NULL,
    `Q3` VARCHAR(1) NOT NULL,
    `Q4` VARCHAR(1) NOT NULL,
    `Q5` VARCHAR(1) NOT NULL,
    `Q6` VARCHAR(1) NOT NULL,
    `Q7` VARCHAR(1) NOT NULL,
    `Q8` VARCHAR(1) NOT NULL,
    `Q9` VARCHAR(1) NOT NULL,
    `Q10` VARCHAR(1) NOT NULL,
    `Q11` VARCHAR(1) NOT NULL,
    `DIMENSIONS` VARCHAR(40) NOT NULL,
    `COMMENT` TEXT NOT NULL,
    `SUBMITTED_AT` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

/*Creating TOOL_DATA Table */
DROP TABLE IF EXISTS `TOOL_DATA`;
CREATE TABLE `TOOL_DATA` (
    `ID` INT AUTO_INCREMENT PRIMARY KEY,
    `SESSION_ID` INT REFERENCES SESSION_DATA(SESSION_ID),
    `TITLE` TEXT NOT NULL,
    `DESCRIPTION` TEXT NOT NULL,
    `OVERALL_CLARITY_VALUE` INT NOT NULL,
    `OVERALL_CLARITY_CONFIDENCE` INT NOT NULL,
    `FEATURE1_VALUE` INT NOT NULL,
    `FEATURE2_VALUE` INT NOT NULL,
    `FEATURE3_VALUE` INT NOT NULL,
    `FEATURE4_VALUE` INT NOT NULL,
    `FEATURE5_VALUE` INT NOT NULL,
    `FEATURE6_VALUE` INT NOT NULL,
    `FEATURE7_VALUE` INT NOT NULL,
    `FEATURE1_CONFIDENCE` INT NOT NULL,
    `FEATURE2_CONFIDENCE` INT NOT NULL,
    `FEATURE3_CONFIDENCE` INT NOT NULL,
    `FEATURE4_CONFIDENCE` INT NOT NULL,
    `FEATURE5_CONFIDENCE` INT NOT NULL,
    `FEATURE6_CONFIDENCE` INT NOT NULL,
    `FEATURE7_CONFIDENCE` INT NOT NULL,
    `SUBMITTED_AT` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)