drop table if exists users;
drop table if exists posts;


create table users(
    id primary key serial,
    name varchar(15) not null,
    last_log timestamp with time zone
);

create table posts(
    id primary key serial,
    title text not null,
    content text,
    options_votes jsonb, 
    auth_id integer not null,
    creation_date timestamp with time zone,
    end_date timestamp with time zone,
    foriegn key (auth_id) references (users.id) on delete cascade  
);

