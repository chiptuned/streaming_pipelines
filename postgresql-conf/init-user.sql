CREATE ROLE your_replication_user WITH REPLICATION LOGIN PASSWORD 'your_password';
GRANT SELECT ON ALL TABLES IN SCHEMA your_schema TO your_replication_user;
