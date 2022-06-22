drop table if exists stuff cascade;
drop table if exists qualification cascade;
drop table if exists medical_card cascade;
drop table if exists patient cascade;
drop table if exists visit cascade;
drop table if exists procedure cascade;
drop table if exists price_list cascade;
drop table if exists stuff_workdays cascade;
drop table if exists visit_stuff cascade;
commit;

create table stuff(
    id             int          primary key,
    name           varchar(50)  not null,
    surname        varchar(50)  not null,
    job            smallint     not null,
    license        varchar(50)  null unique,
    phone          varchar(15)  null,
    interest_rate  real         not null default 0 check (interest_rate between 0 and 1),
    daily_salary   numeric      not null default 0 check (daily_salary >= 0)
);
commit;

-- administrators
insert into stuff (id, name, surname, job, phone, daily_salary) values
        (1, 'Sasha', 'Dolya', 1, '89637458777', 2000),
        (2, 'Masha', 'Florya', 1, '89637398777', 2000);
commit;

--nurses
insert into stuff (id, name, surname, job, license, phone, daily_salary) values
        (3, 'Olya', 'Orlova', 2, 'N412-232', '89633268237', 2500),
        (4, 'Ksenia', 'Frolova', 2, 'N412-664', '89698798745', 2500);
commit;

--doctors
insert into stuff (id, name, surname, job, license, phone, daily_salary, interest_rate) values
        (5, 'Ivan', 'Sergev', 3, 'DOC123-5123', '89633258777', 3000, 0.4),
        (6, 'Lilya', 'Oslo', 3, 'DOC123-4124', '89637398777', 3000, 0.45);
commit;

create table stuff_workdays(
    stuff_id     int        not null,
    date         date       not null,
    unique(stuff_id, date),
    foreign key(stuff_id) references stuff(id)
);
commit;

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


insert into qualification (specialization, organization, stuff_id, date) values
        (1, 'Moscow med', 5, '2012-02-03'),
        (3, 'Kazan med', 6, '2015-07-19');
commit;


create table medical_card(
    id              int             primary key,
    sex             char(1)         not null check (sex in ('M', 'F')),
    blood_type      nchar(3)        not null check (blood_type in (
                                                                'O+', 'O-', 
                                                                'A+', 'A-',
                                                                'B+', 'B-',
                                                                'AB+', 'AB-')),
    birth_date     date            not null,
    allergy        text            null,
    diseases       text            null,
    medicines      text            null
);


create table patient(
    id              int             primary key,
    name            varchar(50)     not null,
    surname         varchar(50)     null,
    phone           varchar(15)     null
);


alter table medical_card
        add foreign key(id) references patient (id)
            DEFERRABLE INITIALLY DEFERRED;

alter table patient
        add foreign key(id) references medical_card (id)
            DEFERRABLE INITIALLY DEFERRED;
commit;

-- patients and med cards
insert into patient values 
        (1, 'Pavel'),
        (2, 'Lera'),
        (3, 'Stepan');

insert into medical_card values 
        (1, 'M', 'O+', '2001-02-10'),
        (2, 'F', 'A-', '2000-05-17'),
        (3, 'M', 'AB-', '1999-03-21');
commit;


create table price_list(
    code        int             primary key,
    name        varchar(255)    not null,
    price       numeric         not null check (price > 0)
);

create table visit(
    id           int             primary key,
    patient_id   int             not null,
    date         date            not null default now(),
    room         int             not null default 1,
    receipt      text            null,
    foreign key (patient_id) references patient(id)
);
commit;

create table visit_stuff(
    visit_id     int        not null,
    stuff_id     int        not null,
    foreign key(visit_id) references visit(id),
    foreign key(stuff_id) references stuff(id),
    unique(visit_id, stuff_id)
);
commit;

create table procedure(
    id          serial          primary key,
    visit_id    int             not null,
    code        int             not null,
    location    smallint        null check (location between 0 and 32),
    quantity    smallint        not null default 1 check (quantity > 0),
    foreign key (code) references price_list(code)
);
commit;


alter table procedure
        add foreign key (visit_id) references visit(id);
commit;

insert into price_list values
    (1, 'анестезия', 1000),
    (2, 'удаление зуба', 2500),
    (3, 'лечение кариеса', 3000),
    (4, 'установка коронки', 5000);
commit;

insert into visit(id, patient_id) values
        (1, 1),
        (2, 2),
        (3, 1),
        (4, 1);
commit;

insert into visit_stuff(visit_id, stuff_id) values
        (1, 5),
        (1, 4),
        (2, 3),
        (2, 4),
        (2, 5);
commit;

insert into procedure (visit_id, code) values
    (1, 1),
    (1, 2),
    (1, 3);
insert into procedure (visit_id, code, quantity) values
    (2, 1, 3),
    (2, 2, 2);
commit;