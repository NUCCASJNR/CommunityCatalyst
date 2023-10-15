-- sql script


CREATE DATABASE IF NOT EXISTS Community_Catalyst_db;
       CREATE USER IF NOT EXISTS 'Community_Catalyst_user'@'localhost' IDENTIFIED BY 'Community_Catalyst_pwd';
              GRANT ALL PRIVILEGES ON Community_Catalyst_db.* TO 'Community_Catalyst_user'@'localhost';
                                      GRANT SELECT ON performance_schema.* TO 'Community_Catalyst_user'@'localhost';
FLUSH PRIVILEGES;