CREATE DATABASE filtered_relation_coalesce_repro;
CREATE USER 'filtered_relation_coalesce_repro'@'localhost' identified with mysql_native_password by 'testing123';
GRANT ALL PRIVILEGES ON filtered_relation_coalesce_repro.* TO 'filtered_relation_coalesce_repro'@'localhost';
