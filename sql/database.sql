create database hatena;

create table recomend_feed (
    no int(10) auto_increment not null,
    collect_day int(10) not null,
    collect_no int(6) not null,
    url text,
    recomend_times int(5) default 1,
    user_no int(10),
    isAdapt tinyint default 0,
    update_time timestamp,
    primary key(
        collect_no,
        collect_day
    ),
    index(
    no,
    collect_no,
    collect_day,
    user_no
    )
);

create table users (
    user_no int(10) auto_increment not null,
    user_name varchar(255) not null,
    recomend_times int(6) default 1 not null,
    register_datetime datetime,
    update_time timestamp,
    primary key(
        user_no
    ),
    index(
        user_no,
        user_name
    )
);



