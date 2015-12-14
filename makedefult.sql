create database stocks;
\c stocks

create table company(
ticker varchar(250),
name varchar(250),
exchange varchar(250),
category varchar(250),
primary key(ticker)
)

create table data(
ticker varchar(250)
dags date
open numeric(8,2),
high numeric(8,2),
low numeric(8,2),
close numeric(8,2),
volume numeric(8,2),
adj close numeric(8,2),
primary key(ticker,dags),
foreign key(ticker) references company(ticker)
)

create table exchange(
exch varchar(250),
fjoldi int,
land varchar(250),
primary key(exch),
foreign key(exch) references company(exch)
)