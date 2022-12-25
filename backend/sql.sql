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
    id int primary key auto_increment,
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
-- 各个用户的权限, 用+组合
-- 按照计划, zvms不会有管理员接口, 所以用户都必须通过数据库操作直接添加
-- 当然你也可以用flask, 这样做: flask --app zvms shell
-- 然后from zvms.models import *
-- from zvms.util import *
-- from zvms.res import *
-- User(...).insert()
-- ...
-- db.session.commit()
set @none = 1;
set @student = 2;
set @teacher = 4;
set @class = 8;
set @manager = 16;
set @auditor = 32;
set @system = 64;
-- 顺便, 班级也是手动加的