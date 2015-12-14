create database stocks;
\c stocks

create table exchange(
exch varchar(250),
fjoldi int,
land varchar(250),
heimsalfa varchar(250),
primary key(exch)
);

create table company(
ticker varchar(250),
name varchar(250),
exchange varchar(250) references exchange(exch),
category varchar(250),
primary key(ticker)
);

create table data(
ticker varchar(250),
dags date,
open float(2),
high float(2),
low float(2),
close float(2),
volume float(2),
adjclose float(2),
primary key(ticker,dags),
foreign key(ticker) references company(ticker)
);