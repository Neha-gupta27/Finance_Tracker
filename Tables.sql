CREATE TABLE categories (	
id INT AUTO_INCREMENT PRIMARY KEY,	
name VARCHAR(100)	
);	
CREATE TABLE transactions (	
id INT AUTO_INCREMENT PRIMARY KEY,	
date DATE,	
description VARCHAR(255),	
amount DECIMAL(10, 2),	
category_id INT,	
FOREIGN KEY (category_id) REFERENCES categories(id)	
);	