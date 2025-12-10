use lab_4;

DELIMITER //
DROP PROCEDURE IF EXISTS sp_add_user//
CREATE PROCEDURE sp_add_user(
    IN p_name VARCHAR(50),
    IN p_surname VARCHAR(60),
    IN p_phone VARCHAR(13),
    IN p_email VARCHAR(45)

)
BEGIN
    INSERT INTO users (name, surname, phone, email)
    VALUES (p_name, p_surname, p_phone, p_email);
END//
DELIMITER ;



DROP TABLE IF EXISTS driver_route;

CREATE TABLE driver_route (
    driver_id BIGINT NOT NULL,
    route_id BIGINT NOT NULL,
    PRIMARY KEY(driver_id, route_id),
    FOREIGN KEY (driver_id) REFERENCES drivers(user_id) ON DELETE CASCADE,
    FOREIGN KEY (route_id) REFERENCES routes(route_id) ON DELETE CASCADE
) ENGINE=InnoDB;

DROP PROCEDURE IF EXISTS sp_link_driver_route_by_names;
DELIMITER //

CREATE PROCEDURE sp_link_driver_route_by_names(
    IN p_name VARCHAR(50),
    IN p_surname VARCHAR(50),
    IN p_start VARCHAR(100),
    IN p_end VARCHAR(100)
)
BEGIN
    DECLARE v_user_id BIGINT;
    DECLARE v_driver_id BIGINT;
    DECLARE v_route_id BIGINT;

    SELECT user_id INTO v_user_id
    FROM users
    WHERE name = p_name AND surname = p_surname
    LIMIT 1;

    IF v_user_id IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User with given name/surname not found';
    END IF;

    SELECT user_id INTO v_driver_id
    FROM drivers
    WHERE user_id = v_user_id
    LIMIT 1;

    IF v_driver_id IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'This user is not a driver';
    END IF;

    SELECT route_id INTO v_route_id
    FROM routes
    WHERE start_location = p_start AND end_location = p_end
    LIMIT 1;

    IF v_route_id IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Route not found';
    END IF;

    INSERT IGNORE INTO driver_route(driver_id, route_id)
    VALUES (v_driver_id, v_route_id);

END//
DELIMITER ;



DELIMITER //
DROP PROCEDURE IF EXISTS sp_insert_noname_package//
CREATE PROCEDURE sp_insert_noname_package()
BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE v_name VARCHAR(50);
    DECLARE v_email VARCHAR(60);
    DECLARE v_phone VARCHAR(15);

    WHILE i <= 10 DO
        SET v_name = CONCAT('Noname', i);
        SET v_email = CONCAT('noname', i, '@test.com');

        SET v_phone = CONCAT(
            '+380',
            LPAD(FLOOR(RAND() * 1000000000), 9, '0')
        );

        -- Вставка користувача
        INSERT INTO users (name, surname, phone, email)
        VALUES (v_name, 'Anonymous', v_phone, v_email);

        SET i = i + 1;
    END WHILE;
END//
DELIMITER ;




DROP FUNCTION IF EXISTS fn_trip_price_stat;
DELIMITER //
CREATE FUNCTION fn_trip_price_stat(
    p_function VARCHAR(10) 
)
RETURNS DECIMAL(15,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_result DECIMAL(15,2);

    IF p_function = 'MAX' THEN
        SELECT MAX(price) INTO v_result FROM trips;
    ELSEIF p_function = 'MIN' THEN
        SELECT MIN(price) INTO v_result FROM trips;
    ELSEIF p_function = 'SUM' THEN
        SELECT SUM(price) INTO v_result FROM trips;
    ELSEIF p_function = 'AVG' THEN
        SELECT AVG(price) INTO v_result FROM trips;
    ELSE
        SET v_result = NULL; 
    END IF;

    RETURN IFNULL(v_result, 0);
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_show_trip_stats;
DELIMITER //
CREATE PROCEDURE sp_show_trip_stats()
BEGIN
    SELECT
        COUNT(*) AS total_trips,
        fn_trip_price_stat('MAX') AS max_price,
        fn_trip_price_stat('MIN') AS min_price,
        fn_trip_price_stat('AVG') AS avg_price,
        fn_trip_price_stat('SUM') AS sum_price
    FROM trips;
END//
DELIMITER ;



DELIMITER //

DROP PROCEDURE IF EXISTS sp_split_table_random;

CREATE PROCEDURE sp_split_table_random(IN p_parent VARCHAR(64))
BEGIN
  DECLARE done INT DEFAULT 0;
  DECLARE v_id VARCHAR(255);
  DECLARE tblA VARCHAR(128);
  DECLARE tblB VARCHAR(128);
  DECLARE ts VARCHAR(32);
  DECLARE pk_col VARCHAR(64);

  -- Визначаємо первинний ключ таблиці
  SET pk_col = (
    SELECT COLUMN_NAME 
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
    WHERE TABLE_NAME = p_parent 
    AND CONSTRAINT_NAME = 'PRIMARY'
    LIMIT 1
  );

  -- Якщо первинний ключ не знайдено, помилка
  IF pk_col IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = CONCAT('No primary key found for table ', p_parent);
  END IF;

  DECLARE cur CURSOR FOR 
    SELECT GROUP_CONCAT(COLUMN_NAME ORDER BY ORDINAL_POSITION SEPARATOR ',')
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
    WHERE TABLE_NAME = p_parent AND CONSTRAINT_NAME = 'PRIMARY';
  
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

  SET ts = DATE_FORMAT(NOW(), '%Y%m%d_%H%i%S');
  SET tblA = CONCAT(p_parent, '_partA_', ts);
  SET tblB = CONCAT(p_parent, '_partB_', ts);

  -- Створюємо копії таблиці
  SET @sqlA = CONCAT('CREATE TABLE `', tblA, '` LIKE `', p_parent, '`;');
  PREPARE stmtA FROM @sqlA;
  EXECUTE stmtA;
  DEALLOCATE PREPARE stmtA;

  SET @sqlB = CONCAT('CREATE TABLE `', tblB, '` LIKE `', p_parent, '`;');
  PREPARE stmtB FROM @sqlB;
  EXECUTE stmtB;
  DEALLOCATE PREPARE stmtB;

  -- Розділяємо дані випадково
  SET @sql = CONCAT(
    'INSERT INTO `', tblA, '` ',
    'SELECT * FROM `', p_parent, '` WHERE MOD(CRC32(`', pk_col, '`), 2) = 0;'
  );
  PREPARE stmt FROM @sql;
  EXECUTE stmt;
  DEALLOCATE PREPARE stmt;

  SET @sql = CONCAT(
    'INSERT INTO `', tblB, '` ',
    'SELECT * FROM `', p_parent, '` WHERE MOD(CRC32(`', pk_col, '`), 2) = 1;'
  );
  PREPARE stmt FROM @sql;
  EXECUTE stmt;
  DEALLOCATE PREPARE stmt;

END//

DELIMITER ;
