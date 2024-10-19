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
    nick_name VARCHAR (250) NOT NULL,
    age INTEGER NOT NULL,
    sex VARCHAR (7) NOT NULL,
    city VARCHAR (100) NOT NULL,
    run_level VARCHAR (8) NOT NULL,
    account_link VARCHAR (255),
    level_partner_need BOOLEAN NOT NULL,
    any_gender BOOLEAN NOT NULL,
    -- use_old_partner BOOLEAN NOT NULL,
    meet_active BOOLEAN NOT NULL,
    id_telegram VARCHAR (255) UNIQUE NOT NULL,
    phone_number  VARCHAR (50),
    link_telegram VARCHAR (255) UNIQUE NOT NULL,
    active BOOLEAN NOT NULL
);

create table if not exists meets(
    id UUID PRIMARY KEY,
    id_first_partner UUID NOT NULL,
    id_second_partner UUID NOT NULL,
    date_algorithm DATE NOT NULL,
    first_partner_meet BOOLEAN,
    second_partner_meet BOOLEAN,
    FOREIGN KEY (id_first_partner) REFERENCES registration(id),
    FOREIGN KEY (id_second_partner) REFERENCES registration(id)
);

create table if not exists comments(
    id UUID PRIMARY KEY,
    id_telegram VARCHAR (255) NOT NULL,
    comment VARCHAR (255)
);

-- create table if not exists comments(
--     id UUID PRIMARY KEY,
--     id_registration UUID,
--     id_meet UUID,
--     is_find_partner BOOLEAN NOT NULL,
--     find_partner BOOLEAN,
--     is_like BOOLEAN,
--     why VARCHAR (255),
--     create_by_system BOOLEAN NOT NULL,
--     FOREIGN KEY (id_registration) REFERENCES registration(id),
--     FOREIGN KEY (id_meet) REFERENCES meets(id)
-- );