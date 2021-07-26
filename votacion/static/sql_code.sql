drop table if exists users cascade;
drop table if exists posts;


create table users(
    id serial primary key ,
    username varchar(15) not null unique,
    email text not null unique,
    image_file text not null default 'batman.png',
    password text not null,
);

create table polls(
    id serial primary key,
    title text not null,
    options_votes jsonb not null, 
    auth_id integer not null references users(id) on delete cascade,
    creation_date  not null,
    end_date  not null
);

