CREATE TABLE class(
    id INT PRIMARY KEY,
    name VARCHAR(5)
);

CREATE TABLE user(
    id INT PRIMARY KEY,
    name VARCHAR(5) UNIQUE,
    class INT,
    pwd VARCHAR(32),
    auth INT
);

CREATE TABLE notice(
    id INT PRIMARY KEY,
    title VARCHAR(32),
    content VARCHAR(1024),
    sender INT,
    sendtime DATETIME,
    deadtime DATETIME
);

CREATE TABLE volunteer(
    id INT PRIMARY KEY,
    name VARCHAR(32),
    description VARCHAR(1024),
    status INT,
    holder INT,
    time DATETIME,
    type SMALLINT,
    reward INT
);

CREATE TABLE stu_vol(
    volunteer INT,
    student INT,
    status SMALLINT,
    thought VARCHAR(1024),
    reason VARCHAR(64),
    reward INT,
    PRIMARY KEY (volunteer, student)
);

CREATE TABLE class_vol(
    volunteer INT,
    class INT,
    max INT,
    PRIMARY KEY (volunteer, class)
);

CREATE TABLE picture(
    identifier VARCHAR(36),
    volunteer INT,
    student INT,
    PRIMARY KEY (identifier, volunteer, student)
);

CREATE TABLE user_notice(
    user INT,
    notice INT,
    PRIMARY KEY (user, notice)
);

CREATE TABLE class_notice(
    class INT,
    notice INT,
    PRIMARY KEY (class, notice)
);

CREATE TABLE school_notice(
    NOTICE INT PRIMARY KEY
);

CREATE TABLE issue(
    id INT PRIMARY KEY,
    time DATETIME,
    author INT,
    content VARCHAR(256)
);