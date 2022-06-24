select 'drop table if exists "' || tablename || '" cascade;' from pg_tables;

drop table if exists salary_job cascade;
drop table if exists stuff cascade;
drop table if exists qualification cascade;
drop table if exists medical_card cascade;
drop table if exists patient cascade;
drop table if exists visit cascade;
drop table if exists procedure cascade;
drop table if exists price_list cascade;
drop table if exists stuff_workdays cascade;
drop table if exists visit_stuff cascade;
drop table if exists job cascade;
commit;

create table job(
    id         int           primary key,
    daily_salary   numeric       not null check (daily_salary > 0),
    job_name       varchar(100) not null
);
commit;



insert into job values
    (1, 2000, 'администратор'),
    (2, 2500, 'медсестра'),
    (3, 3000, 'врач');
commit;


create table stuff(
    id             int          primary key,
    name           varchar(50)  not null,
    surname        varchar(50)  not null,
    job_id         int          not null,
    license        varchar(50)  null unique,
    phone          varchar(15)  not null,
    interest_rate  real         not null default 0 check (interest_rate between 0 and 1),
    foreign key (job_id) references job(id)
);
commit;

-- administrators
insert into stuff (id, name, surname, job_id, phone) values
        (1, 'Саша', 'Доля', 1, '89637458777'),
        (2, 'Маша', 'Флоря', 1, '89637398777');
commit;

--nurses
insert into stuff (id, name, surname, job_id, license, phone) values
        (3, 'Оля', 'Орлова', 2, 'N412-232', '89633268237'),
        (4, 'Ксения', 'Фролова', 2, 'N412-664', '89698798745');
commit;

--doctors
insert into stuff (id, name, surname, job_id, license, phone, interest_rate) values
        (5, 'Иван', 'Сергев', 3, 'DOC123-5123', '89633258777', 0.4),
        (6, 'Арина', 'Жук', 3, 'DOC123-4124', '89637398777', 0.45);
commit;

create table stuff_workdays(
    stuff_id     int        not null,
    date         date       not null,
    unique(stuff_id, date),
    constraint fk_stuff
        foreign key(stuff_id) references stuff(id)
);
commit;

insert into stuff_workdays(stuff_id, date)
select 1, * from generate_series('2022-06-01'::date, '2022-06-22'::date, '2 day'::interval);
commit;


insert into stuff_workdays(stuff_id, date)
select 2, * from generate_series('2022-06-02'::date, '2022-06-23'::date, '2 day'::interval);
commit;

insert into stuff_workdays(stuff_id, date)
select 3, * from generate_series('2022-06-01'::date, '2022-06-23'::date, '2 day'::interval);
commit;

insert into stuff_workdays(stuff_id, date)
select 4, * from generate_series('2022-06-02'::date, '2022-06-23'::date, '2 day'::interval);
commit;

insert into stuff_workdays(stuff_id, date)
select 5, * from generate_series('2022-06-01'::date, '2022-06-23'::date, '2 day'::interval);
commit;


insert into stuff_workdays(stuff_id, date)
select 6, * from generate_series('2022-06-02'::date, '2022-06-23'::date, '2 day'::interval);
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
        (1, 'МГМУ им. Сеченова', 5, '2012-02-03'),
        (3, 'КГМУ', 6, '2015-07-19');
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
        (1, 'Павел'),
        (2, 'Валерия'),
        (3, 'Степан');

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


select id, license from stuff where license is null;

create or replace function check_stuff()
    returns trigger
as $check_stuff$
begin
    if not exists(select id, license from stuff where id=new.stuff_id and license is not null) then
        raise exception 'Cannot hold a visit without medical license';
    end if;
    if not exists(
        select date from visit where visit.id = new.visit_id
        intersect
        select date from stuff_workdays s where s.stuff_id=new.stuff_id
    ) then
        raise exception 'Stuff cannot hold a visit on a non-working day';
    end if;
    return new;
end;
$check_stuff$ language plpgsql;

create trigger check_stuff before insert or update on visit_stuff
    for each row execute function check_stuff();

-- select license from stuff;

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

insert into visit(id, patient_id, date) values
        (1, 1, '2022-06-01'),
        (2, 2, '2022-06-02'),
        (3, 1, '2022-06-03'),
        (4, 1, '2022-06-04');
commit;

insert into visit_stuff(visit_id, stuff_id) values
        (1, 5), --06-01: 3, 5
        (1, 3), 
        (2, 4),  -- 06-02: 4, 6
        (2, 6);
commit;


insert into procedure (visit_id, code) values
    (1, 1),
    (1, 2),
    (1, 3);
insert into procedure (visit_id, code, quantity) values
    (2, 1, 3),
    (2, 2, 2);
commit;


select * from job;
-- select * from stuff s inner join salary_job j on j.job =s.job 

-- select * from visit v inner join visit_stuff s on v.id = s.visit_id left join stuff_workdays w on s.stuff_id = w.stuff_id and w.date = v.date;