drop table if exists stuff cascade;
drop table if exists qualification cascade;
drop table if exists medical_card cascade;
drop table if exists patient cascade;
drop table if exists visit cascade;


create table stuff(
        id             int          primary key,
        name           varchar(50)  not null,
        surname        varchar(50)  not null,
        job            smallint     not null,
        license        varchar(50)  null unique,
        phone          varchar(15)  null,
        interest_rate  real         null,
        salary         numeric      null
);
commit;

-- administrators
insert into stuff (id, name, surname, job, phone, salary) values
        (1, 'Sasha', 'Dolya', 1, '89637458777', 60000),
        (2, 'Masha', 'Florya', 1, '89637398777', 60000);
commit;


--nurses
insert into stuff (id, name, surname, job, license, phone, salary) values
        (3, 'Olya', 'Orlova', 2, 'N412-232', '89633268237', 50000),
        (4, 'Ksenia', 'Frolova', 2, 'N412-664', '89698798745', 50000);
commit;

--doctors
insert into stuff (id, name, surname, job, license, phone, salary, interest_rate) values
        (5, 'Ivan', 'Sergev', 3, 'DOC123-5123', '89633258777', 30000, 0.4),
        (6, 'Lilya', 'Oslo', 3, 'DOC123-4124', '89637398777', 30000, 0.45);
commit;

insert into qualification


insert into 


create table qualification(
    id                serial        primary key,
    specialization    smallint      not null,
    stuff_id          int           not null,
    organization      varchar(100)  not null,
    date              date          null,
    constraint fk_stuff 
            foreign key(stuff_id) references stuff(id)
);
commit;

create table medical_card(
    id              int             primary key,
    sex             char(1)         not null check (sex in ('M', 'F')),
    blood_type      nchar(3)        not null check (blood_type in ('O+', 'A+', 'B+', 'AB+',
                                                       'O-', 'A-', 'B-', 'AB-')),
    birth_date     date            not null,
    allergy        text            null,
    diseases       text            null,
    medicines      text            null
);
commit;

create table patient(
    id              int             primary key,
    name            varchar(50)     not null,
    surname         varchar(50)     null,
    phone           varchar(15)     null
);
commit;

alter table medical_card
        add foreign key(id) references patient (id)
            DEFERRABLE INITIALLY DEFERRED;

alter table patient
        add foreign key(id) references medical_card (id)
            DEFERRABLE INITIALLY DEFERRED;

insert into patient values 
        (1, 'Pavel'),
        (2, 'Lera'),
        (3, 'Stepan');
insert into medical_card values 
        (1, 'M', 'O+', '2001-02-10'),
        (2, 'F', 'A-', '2000-05-17'),
        (3, 'M', 'AB-', '1999-03-21');
commit;

create table visit(
    id          serial          primary key,
    patient_id  int             not null,
    stuff_id    int             not null,
    date        date            not null,
    room        int             null,
    receipt     text            null,
    foreign key (patient_id) references patient(id),
    foreign key (stuff_id) references stuff(id)
);
commit;

-- insert into visit (patient_id, stuff_id, date) values
--         (1, 1, '2020-02-02'),
--         (1, 2, '2020-03-03');
-- commit;