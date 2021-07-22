drop table if exists users cascade;
drop table if exists posts;


create table users(
    id serial primary key ,
    username varchar(15) not null unique,
    email text not null unique,
    password text not null,
    last_login timestamp with time zone not null
);

create table posts(
    id serial primary key,
    title text not null,
    content text,
    options_votes jsonb not null, 
    auth_id integer not null references users(id) on delete cascade,
    creation_date timestamp without time zone not null,
    end_date timestamp with time zone not null
);

