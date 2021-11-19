DROP SCHEMA IF EXISTS online_store;
CREATE SCHEMA `online_store` ;
USE online_store;

CREATE TABLE `online_store`.`orders` (
  `order_id` INT NOT NULL,
  `user_id` INT NULL,
  `address_id` INT NULL,
  `total_price` FLOAT NULL,
  PRIMARY KEY (`order_id`));

CREATE TABLE `online_store`.`order_details` (
  `order_id` INT NOT NULL,
  `inventory_id` INT NOT NULL,
  `amount` INT NOT NULL,
  `price` INT NOT NULL,
  INDEX `order_inventory_idx` (`order_id` ASC) VISIBLE,
  CONSTRAINT `order_inventory`
    FOREIGN KEY (`order_id`)
    REFERENCES `online_store`.`orders` (`order_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- INSERT INTO orders VALUES (1, 1, 11, 29.99);
-- INSERT INTO orders VALUES (2, 2, 22, 54.98);

-- INSERT INTO order_details VALUES (1, 1, 1, 29.99);
-- INSERT INTO order_details VALUES (2, 1, 1, 29.99);
-- INSERT INTO order_details VALUES (2, 2, 1, 24.99);

