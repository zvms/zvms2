CREATE TABLE class(
    id INT PRIMARY KEY,
    name VARCHAR(5)
); 
CREATE TABLE user(
    id INT PRIMARY KEY,
    name VARCHAR(5),
    class INT, 
    pwd CHAR(32), 
    auth INT
);
CREATE TABLE notice(
    id INT PRIMARY KEY auto_increment, 
    title VARCHAR(32), 
    content VARCHAR(1024), 
    sender INT, 
    deadtime datetime
);
CREATE TABLE volunteer(
    id INT PRIMARY KEY auto_increment, 
    name VARCHAR(32), 
    description VARCHAR(1024), 
    status SMALLINT,
    holder INT, time datetime, 
    type SMALLINT, 
    reward INT
);
CREATE TABLE stu_vol(
    stu_id INT, 
    vol_id INT, 
    status SMALLINT, 
    thought VARCHAR(1024), 
    reason VARCHAR(1024), 
    reward INT, 
    PRIMARY KEY(stu_id, vol_id)
);
CREATE TABLE picture(
    stu_id INT, 
    vol_id INT, 
    hash CHAR(32), 
    PRIMARY KEY(stu_id, vol_id, hash)
);
CREATE TABLE class_vol(
    class_id INT, 
    vol_id INT, 
    max INT, 
    PRIMARY KEY(class_id, vol_id)
); 
CREATE TABLE user_notice(
    user_id INT, 
    notice_id INT, 
    PRIMARY KEY(user_id, notice_id)
);
CREATE TABLE class_notice(
    class_id INT, 
    notice_id INT, 
    PRIMARY KEY(class_id, notice_id)
);
CREATE TABLE school_notice(
    notice_id INT PRIMARY KEY
);
CREATE TABLE log(
    id INT PRIMARY KEY auto_increment
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
SET @none = 1;
SET @student = 2;
SET @teacher = 4;
SET @class = 8;
SET @manager = 16;
SET @auditor = 32;
SET @system = 64;
-- 顺便, 班级也是手动加的