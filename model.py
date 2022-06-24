from datetime import datetime
import json

class Entity:
    def __init__(self) -> None:
        pass
    
    def get_data(self):
        return dict((k, v) for k, v in self.__dict__.items() if v is not None)
    
    def get_row(self):
        return tuple(v for v in self.__dict__.values())

from enum import Enum
class Job(Entity):
    def __init__(
        self,
        id: int,
        daily_salary: float,
        name: str,
    ) -> None:

        super().__init__()
        self.id = int(id)
        self.daily_salary = float(daily_salary)
        self.name = str(name)
    
# create table job(
#     id         int           primary key,
#     daily_salary   numeric       not null check (daily_salary > 0),
#     name           varchar(100) not null
# );
# commit;


class Specialization(Enum):
    ORTHODONTIST = 1
    THERAPIST = 2
    ORTHOPEDIST = 3
    SURGEON = 4

    def __str__(self):
        return self.name


class Stuff(Entity):
    def __init__(
        self,
        id: int,
        name: str,
        surname: str,
        job: int,
        license: str = None,
        phone: str = None,
        interest_rate: float = None,
    ) -> None:

        super().__init__()
        self.id = int(id)
        self.name = str(name)
        self.surname = str(surname)
        self.job = int(job)

        self.license = str(license) if license is not None else ''
        self.phone = str(phone)
        self.interest_rate = float(interest_rate)

    def get_name(self, job_name: dict):
        if job_name is not None:
            return f'{self.id} {job_name[self.job]} {self.name} {self.surname}'
        return f'{self.id} {self.name} {self.surname}'
class Qualification(Entity):
    def __init__(
        self,
        id: int,
        specialization: Specialization,
        organization: str,
        stuff_id: int,
        date: datetime = None,
        description: str = None,
    ) -> None:

        super().__init__()
        self.id = id
        self.specialization = specialization.value
        self.organization = organization
        self.stuff_id = stuff_id
        self.date = date
        self.description = description

class Visit(Entity):
    def __init__(
        self,
        patient_id: int,
        stuff_id: int,
        date: str = None
    ) -> None:
        super().__init__()
            