create table class(
    id int primary key,
    name varchar(5)
); 
create table user(
    id int primary key,
    name varchar(5),
    class int, 
    pwd char(32), 
    auth int
);
create table notice(
    id int primary key auto_increment, 
    title varchar(32), 
    content varchar(1024), 
    sender int, 
    deadtime datetime
);
create table volunteer(
    id int primary key auto_increment, 
    name varchar(32), 
    description varchar(1024), 
    holder int, time datetime, 
    type smallint, 
    reward int
);
create table stu_vol(
    stu_id int, 
    vol_id int, 
    status smallint, 
    thought varchar(1024), 
    reason varchar(1024), 
    reward int, 
    primary key(stu_id, vol_id)
);
create table picture(
    stu_id int, 
    vol_id int, 
    hash char(32), 
    primary key(stu_id, vol_id)
);
create table class_vol(
    class_id int, 
    vol_id int, 
    max int, 
    primary key(class_id, vol_id)
); 
create table user_notice(
    user_id int, 
    notice_id int, 
    primary key(user_id, notice_id)
);
create table class_notice(
    class_id int, 
    notice_id int, 
    primary key(class_id, notice_id)
);
create table school_notice(
    notice_id int primary key
);
create table log(
    id int primary key auto_increment
);