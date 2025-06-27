-- Create database and user if they don't exist
DO $$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'dhikra_user') THEN
      CREATE ROLE dhikra_user LOGIN PASSWORD 'dhikra_password';
   END IF;
END
$$;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE dhikra_db TO dhikra_user;
GRANT ALL ON SCHEMA public TO dhikra_user;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO dhikra_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO dhikra_user; 