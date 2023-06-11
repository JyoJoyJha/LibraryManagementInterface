# LibraryManagementInterface
Library Management: MySQL + Python (Interface Project) Keeps Track of all the Transactions in the library- Issue and Return of books along with Fine management
This is a Python and a MySQL Interface Project

This Project required few Beforehand SQL Queriess to be run at the MySQL Shell
The SQL Queries are as follows:

**TABLES/DATABASES:**

MEMBERS:
create table MEMBERS (
m_id int primary key,
fname varchar(25),
lname varchar(35),
DOB date,
mgender varchar(10),
mphone bigint,
check (floor(datediff('2022-01-01', DOB)/365)>13)
);

BOOKS:
Create table BOOKS (
ISBN int primary key,
bname varchar(125),
Author varchar(55),
Publisher varchar(45),
Edition int
Status char(1) default 'f',
);

ISSUE:
create table Issue (
m_id int,
ISBN int,
issue_date date,
return_date_e date default '0000-00-00',
return_date_a date default '0000-00-00',
return_stat varchar(10) default="NR"
primary key (m_id, ISBN, issue_date),
foreign key (m_id) references MEMBERS(m_id) on delete cascade,
foreign key (ISBN) references BOOKS(ISBN) on delete cascade
);

FINE:
create table FINE (
m_id int primary key,
fine_amt int default 0,
foreign key(m_id) references MEMBERS(m_id) on delete cascade
);

**TRIGGER:**
When A book is issued, change the status of the book:
create trigger change_stat before insert on issue
for each row update books b set
b.status='t'
where b.ISBN=new.ISBN;

The Additional Documentation is provided in the Repository as a PDF File. 
For additional information, Do check the Documnetation report
