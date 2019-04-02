USE cashbook;

CREATE TABLE `collection` (
  `id` INT(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) DEFAULT NULL,
  `month` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `check` BIT(2) NOT NULL DEFAULT b'0',
  KEY `id` (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `book` (
  `id` INT(11) unsigned NOT NULL AUTO_INCREMENT,
  `summary` VARCHAR(255) DEFAULT NULL,
  `kept` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `incomes` INT(11) DEFAULT 0,
  `expenses` INT(11) DEFAULT 0,
  KEY `id` (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `admin` (
  `id` INT(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) DEFAULT NULL,
  `password` VARCHAR(255) DEFAULT NULL,
  KEY `id` (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOAD DATA LOCAL INFILE '/docker-entrypoint-initdb.d/members.csv' INTO TABLE cashbook.collection FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES (@1) SET `name`=@1;

LOAD DATA LOCAL INFILE '/docker-entrypoint-initdb.d/admin.csv' INTO TABLE cashbook.admin FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES (@1,@2) SET `name`=@1, `password`=@2;
