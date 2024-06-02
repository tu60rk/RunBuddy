CREATE SCHEMA IF NOT EXISTS content;
ALTER ROLE CURRENT_USER SET search_path TO content,public;

-- DROP DATABASE IF EXISTS run_database;
-- CREATE DATABASE run_database;
GRANT ALL PRIVILEGES ON DATABASE run_database TO CURRENT_USER;


-- Create need tables for work app
create table if not exists registration(
    id UUID PRIMARY KEY,
    name VARCHAR (50) NOT NULL,
    last_name VARCHAR (50) NOT NULL,
    age INTEGER NOT NULL,
    sex VARCHAR (7) NOT NULL,
    city VARCHAR (100) NOT NULL,
    run_level VARCHAR (8) NOT NULL,
    account_link VARCHAR (255) NOT NULL,
    level_partner_need BOOLEAN NOT NULL,
    any_gender BOOLEAN NOT NULL,
    meet_active BOOLEAN NOT NULL,
    id_telegram INTEGER UNIQUE NOT NULL, 
    link_telegram VARCHAR (255) UNIQUE NOT NULL
);

create table if not exists meets(
    id UUID PRIMARY KEY,
    id_first_partner UUID NOT NULL,
    id_second_partner UUID NOT NULL,
    datetime_algorithm TIMESTAMP NOT NULL,
    FOREIGN KEY (id_first_partner) REFERENCES registration(id),
    FOREIGN KEY (id_second_partner) REFERENCES registration(id)
);

create table if not exists comments(
    id UUID PRIMARY KEY,
    id_registration UUID,
    -- id_partner UUID 
    find_partner BOOLEAN,
    is_like BOOLEAN,
    why VARCHAR (255),
    FOREIGN KEY (id_registration) REFERENCES registration(id)
    -- FOREIGN KEY (id_partner) REFERENCES registration(id)
);