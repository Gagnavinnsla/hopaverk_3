create database stocks;
\c stocks

create table company(
ticker varchar(250),
name varchar(250),
exchange varchar(250),
category varchar(250),
primary key(ticker)
)

create table gogn(
open numeric(8,2),
high numeric(8,2),
low numeric(8,2),
close numeric(8,2),
volume numeric(8,2),
adj close numeric(8,2)
)