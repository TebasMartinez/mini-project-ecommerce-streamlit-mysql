-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema miniproject_ecommerce
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema miniproject_ecommerce
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `miniproject_ecommerce` DEFAULT CHARACTER SET utf8 ;
USE `miniproject_ecommerce` ;

-- -----------------------------------------------------
-- Table `miniproject_ecommerce`.`products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `miniproject_ecommerce`.`products` (
  `product_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `category` VARCHAR(45) NOT NULL,
  `price` FLOAT NOT NULL,
  `stock` INT NOT NULL,
  PRIMARY KEY (`product_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `miniproject_ecommerce`.`customers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `miniproject_ecommerce`.`customers` (
  `customer_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`customer_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `miniproject_ecommerce`.`orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `miniproject_ecommerce`.`orders` (
  `order_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `order_date` DATETIME NOT NULL,
  `quantity` INT NOT NULL,
  `total_amount` FLOAT NOT NULL,
  `customer_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`order_id`),
  INDEX `fk_orders_customers1_idx` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_orders_customers1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `miniproject_ecommerce`.`customers` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `miniproject_ecommerce`.`orders_products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `miniproject_ecommerce`.`orders_products` (
  `product_id` INT UNSIGNED NOT NULL,
  `order_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`product_id`, `order_id`),
  INDEX `fk_products_has_orders_orders1_idx` (`order_id` ASC) VISIBLE,
  INDEX `fk_products_has_orders_products1_idx` (`product_id` ASC) VISIBLE,
  CONSTRAINT `fk_products_has_orders_products1`
    FOREIGN KEY (`product_id`)
    REFERENCES `miniproject_ecommerce`.`products` (`product_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_products_has_orders_orders1`
    FOREIGN KEY (`order_id`)
    REFERENCES `miniproject_ecommerce`.`orders` (`order_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
