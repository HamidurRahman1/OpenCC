
drop schema if exists opencc_db;

create schema opencc_db;

use opencc_db;

drop tables if exists users, terms, subjects, requests;

create table users
(
	user_id int primary key auto_increment,
    phone_num varchar(9) not null unique
);

create table terms
(
	term_id int primary key auto_increment,
    term_name varchar(11) not null unique,
    term_value varchar(4) not null unique
);

create table subjects
(
	subject_id int primary key auto_increment,
    subject_code varchar(4) not null,
    subject_name varchar(10) not null,
    unique key (subject_code, subject_name)
);

create table requests
(
    request_id int primary key auto_increment,
    fk_user_id int not null,
    fk_term_id int not null,
    fk_subject_id int not null,
    class_num_5_digit int not null,
    foreign key (fk_user_id) references users(user_id),
    foreign key (fk_term_id) references terms(term_id),
    foreign key (fk_subject_id) references subjects(subject_id),
    unique key(fk_user_id, fk_term_id, fk_subject_id, class_num_5_digit)
);