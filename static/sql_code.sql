drop table if exists users cascade;
drop table if exists polls;


create table users(
    id serial primary key ,
    username varchar(15) not null unique,
    email text not null unique,
    image_file text not null ,
    password text not null
);

create table polls(
    id serial primary key,
    title text not null,
    options_votes jsonb not null, 
    auth_id integer not null references users(id) on delete cascade,
    emails text[],
    creation_date  text not null,
    end_date  text not null
);

