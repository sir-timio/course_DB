drop table if exists salary_job cascade;
drop table if exists stuff cascade;
drop table if exists qualification cascade;
drop table if exists medical_card cascade;
drop table if exists patient cascade;
drop table if exists visit cascade;
drop table if exists treatment cascade;
drop table if exists price_list cascade;
drop table if exists stuff_workdays cascade;
drop table if exists visit_stuff cascade;
drop table if exists job cascade;
commit;

create table job(
    id             int           primary key,
    job_name       varchar(100)  not null,
    daily_salary   numeric       not null check (daily_salary > 0),
    unique(job_name)
);
commit;



insert into job (id, daily_salary, job_name) values
    (1, 2000, 'администратор'),
    (2, 2500, 'медсестра'),
    (3, 3000, 'врач');
commit;


create table stuff(
    id             int          primary key,
    name           varchar(50)  not null,
    surname        varchar(50)  not null,
    phone          varchar(15)  not null,
    job_id         int          not null,
    license        varchar(50)  null,
    interest_rate  real         not null default 0 check (interest_rate between 0 and 1),
    foreign key (job_id) references job(id),
    unique(phone),
    unique(license)
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
        (6, 'Арина', 'Жук', 3, 'DOC123-4124', '89617391777', 0.45);
commit;

create table stuff_workdays(
    id           serial     primary key,
    stuff_id     int        not null,
    date         date       not null,
    unique(stuff_id, date),
    foreign key(stuff_id) references stuff(id)
);
commit;


create table qualification(
    id                serial        primary key,
    stuff_id          int           not null,
    specialization    smallint      not null,
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
    phone           varchar(15)     not null,
    unique(phone)
);


alter table medical_card
        add foreign key(id) references patient (id)
            DEFERRABLE INITIALLY DEFERRED;

alter table patient
        add foreign key(id) references medical_card (id)
            DEFERRABLE INITIALLY DEFERRED;
commit;

-- patients and med cards
insert into patient (id, name, phone) values 
        (1, 'Павел', '89634386237'),
        (2, 'Валерия', '89333162239'),
        (3, 'Степан', '89635289217');
insert into patient values
        (4, 'Виктор', 'Викторов', '89638260230');

insert into medical_card values 
        (1, 'M', 'O+', '2001-02-10'),
        (2, 'F', 'A-', '2000-05-17'),
        (3, 'M', 'AB-', '1999-03-21'),
        (4, 'M', 'AB-', '1978-01-20');
commit;


create table price_list(
    code        int             primary key,
    name        varchar(255)    not null,
    price       numeric         not null check (price > 0),
    unique(name)
);

create table visit(
    id           serial          primary key,
    patient_id   int             not null,
    doctor_id    int             not null,
    date         date            not null default now(),
    time         time            not null default date_trunc('minutes', now()),
    room         smallint        not null default 1,
    receipt      text            null,
    foreign key (patient_id) references patient(id),
    foreign key (doctor_id) references stuff(id),
    unique (id, doctor_id),
    unique (id, patient_id)
);
commit;

create or replace function check_stuff()
    returns trigger
as $check_stuff$
begin
    if not exists(select id, job_id from stuff where id=new.doctor_id and job_id=3) then
        raise exception 'Only doctor can hold a visit';
    end if;
    if new.date not in(
        select date from stuff_workdays s where s.stuff_id=new.doctor_id
    ) then
        raise exception 'Doctor cannot hold a visit on a non-working day';
    end if;
    return new;
end;
$check_stuff$ language plpgsql;

create trigger check_stuff before insert or update on visit
    for each row execute function check_stuff();


create table treatment(
    id          serial          primary key,
    visit_id    int             not null,
    code        int             not null,
    location    smallint        null check (location between 0 and 32),
    quantity    smallint        not null default 1 check (quantity > 0),
    foreign key (code) references price_list(code),
    foreign key (visit_id) references visit(id)
);
commit;

insert into price_list values
    (1, 'анестезия', 1000),
    (2, 'удаление зуба', 2500),
    (3, 'лечение кариеса', 3000),
    (4, 'установка коронки', 5000);
commit;

insert into visit(patient_id, doctor_id, date) values
        (1, 5, '2022-06-01'),
        (2, 6,'2022-06-02'),
        (1, 5, '2022-06-03'),
        (1, 6, '2022-06-04');
commit;

insert into treatment (visit_id, code) values
    (1, 1),
    (1, 2),
    (1, 3);

insert into treatment (visit_id, code, quantity) values
    (2, 1, 3),
    (2, 2, 2),
    (3, 1, 2),
    (3, 2, 2),
    (4, 1, 2),
    (4, 2, 2);
commit;
