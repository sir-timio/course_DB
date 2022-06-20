drop table if exists stuff cascade;
drop table if exists qualification cascade;
drop table if exists medical_card cascade;
drop table if exists patient cascade;



create table stuff(
        id             serial       primary key,
        name           varchar(50)  not null,
        surname        varchar(50)  not null,
        job            smallint     not null,
        license        varchar(50)  null unique,
        phone          varchar(15)  null,
        interest_rate  real         null,
        salary         numeric      null
);

create table qualification(
    id                serial        primary key,
    specialization    smallint      not null,
    stuff_id          int           not null unique,
    organization      varchar(100)  not null,
    date              date          null,
    constraint fk_stuff 
            foreign key(stuff_id) references stuff(id)
);

create table medical_card(
    id              serial          primary key,
    patient_id      int             not null, 
    sex             char(1)         not null check (sex in ('M', 'F')),
    blood_type      nchar(3)        not null check (blood_type in ('O+', 'A+', 'B+', 'AB+',
                                                       'O-', 'A-', 'B-', 'AB-')),
     allergy        text            null,
     diseases       text            null,
     medicines      text            null
);

create table patient(
    id              serial          primary key,
    name            varchar(50)     not null,
    surname         varchar(50)     null,
    medical_card_id  int             not null unique,
    constraint fk_medical_card_id
        foreign key(medical_card_id) references medical_card(id)
);
