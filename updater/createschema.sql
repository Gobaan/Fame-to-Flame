DROP DATABASE IF EXISTS fydp_db;

create user 'fydp'@'%' identified by 'fydp';
create database fydp_db character set utf8;
grant all privileges on fydp_db.* to 'fydp'@'%';

-- table for storing feed items
-- TODO: create foreign key on feedurl column
create table fydp_db.feeditem (
  guid varchar(255) not null,
  feedurl varchar(255) not null,
  content text not null,
  title varchar(255),
  link varchar(255),
  author varchar(255),
  comments varchar(255),
  published timestamp,
  primary key (guid)
);

-- TODO: create table to store feed urls
