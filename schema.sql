-- Disable foreign key checks for dropping tables
SET FOREIGN_KEY_CHECKS = 0;

-- Drop tables if they exist
DROP TABLE IF EXISTS `Tracking_Detail`;
DROP TABLE IF EXISTS `Payment`;
DROP TABLE IF EXISTS `Order_Items`;
DROP TABLE IF EXISTS `Order`;
DROP TABLE IF EXISTS `Cart_Items`;
DROP TABLE IF EXISTS `Cart`;
DROP TABLE IF EXISTS `Product`;
DROP TABLE IF EXISTS `Product_Category`;
DROP TABLE IF EXISTS `Seller`;
DROP TABLE IF EXISTS `Address`;
DROP TABLE IF EXISTS `User`;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- 1. User
CREATE TABLE `User` (
    `u_id` INT AUTO_INCREMENT PRIMARY KEY,
    `first_name` VARCHAR(100) NOT NULL,
    `last_name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(150) UNIQUE NOT NULL,
    `password_hash` VARCHAR(255) NOT NULL,
    `phone_number` VARCHAR(20)
);

-- 2. Address
CREATE TABLE `Address` (
    `address_id` INT AUTO_INCREMENT PRIMARY KEY,
    `u_id` INT NOT NULL,
    `city` VARCHAR(100) NOT NULL,
    `state` VARCHAR(100) NOT NULL,
    FOREIGN KEY (`u_id`) REFERENCES `User`(`u_id`) ON DELETE CASCADE
);

-- 4. Seller
CREATE TABLE `Seller` (
    `seller_id` INT AUTO_INCREMENT PRIMARY KEY,
    `u_id` INT UNIQUE NOT NULL,
    `company_name` VARCHAR(150) NOT NULL,
    FOREIGN KEY (`u_id`) REFERENCES `User`(`u_id`) ON DELETE CASCADE
);

-- 5. Product_Category
CREATE TABLE `Product_Category` (
    `c_id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) UNIQUE NOT NULL
);

-- 3. Product
CREATE TABLE `Product` (
    `p_id` INT AUTO_INCREMENT PRIMARY KEY,
    `seller_id` INT NOT NULL,
    `c_id` INT,
    `p_name` VARCHAR(200) NOT NULL,
    `p_price` DECIMAL(10, 2) NOT NULL,
    `p_description` TEXT,
    `p_image_url` VARCHAR(500),
    `p_stock` INT NOT NULL DEFAULT 0,
    FOREIGN KEY (`seller_id`) REFERENCES `Seller`(`seller_id`) ON DELETE CASCADE,
    FOREIGN KEY (`c_id`) REFERENCES `Product_Category`(`c_id`) ON DELETE SET NULL
);

-- 6. Cart
CREATE TABLE `Cart` (
    `cart_id` INT AUTO_INCREMENT PRIMARY KEY,
    `u_id` INT UNIQUE NOT NULL,
    FOREIGN KEY (`u_id`) REFERENCES `User`(`u_id`) ON DELETE CASCADE
);

-- 7. Cart_Items
CREATE TABLE `Cart_Items` (
    `cart_id` INT NOT NULL,
    `p_id` INT NOT NULL,
    `quantity` INT NOT NULL DEFAULT 1,
    PRIMARY KEY (`cart_id`, `p_id`),
    FOREIGN KEY (`cart_id`) REFERENCES `Cart`(`cart_id`) ON DELETE CASCADE,
    FOREIGN KEY (`p_id`) REFERENCES `Product`(`p_id`) ON DELETE CASCADE
);

-- 8. Order
CREATE TABLE `Order` (
    `order_id` INT AUTO_INCREMENT PRIMARY KEY,
    `u_id` INT NOT NULL,
    `order_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `order_amount` DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (`u_id`) REFERENCES `User`(`u_id`) ON DELETE CASCADE
);

-- Extra: Order_Items (Needed for "Order contains Products")
CREATE TABLE `Order_Items` (
    `order_id` INT NOT NULL,
    `p_id` INT NOT NULL,
    `quantity` INT NOT NULL,
    `price_at_purchase` DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (`order_id`, `p_id`),
    FOREIGN KEY (`order_id`) REFERENCES `Order`(`order_id`) ON DELETE CASCADE,
    FOREIGN KEY (`p_id`) REFERENCES `Product`(`p_id`) ON DELETE CASCADE
);

-- 9. Payment
CREATE TABLE `Payment` (
    `payment_id` INT AUTO_INCREMENT PRIMARY KEY,
    `u_id` INT NOT NULL,
    `order_id` INT NOT NULL,
    `method` VARCHAR(50) NOT NULL,
    `amount` DECIMAL(10, 2) NOT NULL,
    `payment_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`u_id`) REFERENCES `User`(`u_id`) ON DELETE CASCADE,
    FOREIGN KEY (`order_id`) REFERENCES `Order`(`order_id`) ON DELETE CASCADE
);

-- 10. Tracking_Detail
CREATE TABLE `Tracking_Detail` (
    `t_id` INT AUTO_INCREMENT PRIMARY KEY,
    `order_id` INT NOT NULL,
    `status` VARCHAR(50) NOT NULL,
    `update_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`order_id`) REFERENCES `Order`(`order_id`) ON DELETE CASCADE
);
