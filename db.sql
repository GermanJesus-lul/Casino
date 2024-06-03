CREATE TABLE `users` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `username` VARCHAR(255),
  `password` VARCHAR(255),
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `balance` BIGINT
);

CREATE TABLE `sessions` (
  `token` VARCHAR(16) PRIMARY KEY,
  `user_id` BIGINT,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `history` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `user_id` BIGINT,
  `value` BIGINT,
  `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `game_id` INT,
  `field_1` DOUBLE,
  `field_2` VARCHAR(255)
);

CREATE TABLE `games` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255),
  `games_played` BIGINT,
  `total_value` BIGINT
);

ALTER TABLE `sessions` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `history` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `history` ADD FOREIGN KEY (`game_id`) REFERENCES `games` (`id`);
