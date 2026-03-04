CREATE DATABASE IF NOT EXISTS client_contact_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE client_contact_db;

CREATE TABLE IF NOT EXISTS clients (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  code CHAR(6) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_clients_code (code),
  INDEX idx_clients_name (name)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS contacts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  surname VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_contacts_email (email),
  INDEX idx_contacts_fullname (surname, name)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS client_contact (
  client_id INT NOT NULL,
  contact_id INT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (client_id, contact_id),
  INDEX idx_cc_contact (contact_id),
  CONSTRAINT fk_cc_client FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE,
  CONSTRAINT fk_cc_contact FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE
) ENGINE=InnoDB;
