create table stuff(
        id             serial       primary key,
        name           text         not null,
        surname        text         not null,
        job            smallint     not null,
        license        varchar(50)  null,
        phone          varchar(15)  null,
        birth_date     time         null,
        interest_rate  real         null,
        salary         money        null
    );