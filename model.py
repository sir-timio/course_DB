from datetime import datetime
import json

class Entity:
    def __init__(self) -> None:
        pass
    
    def get_data(self):
        return dict((k, v) for k, v in self.__dict__.items() if v is not None)

from enum import Enum
class Job(Enum):
    ADMINISTRATOR = 1
    NURSE = 2
    DOCTOR = 3

    def __str__(self):
        return self.name


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
        job: Job,
        name: str,
        surname: str,
        license: str = None,
        phone: str = None,
        salary: int = None,
        interest_rate: float = None,
    ) -> None:

        super().__init__()
        self.id = id
        self.name = name
        self.surname = surname
        self.job = job.value

        if self.job in [Job.ADMINISTRATOR.value]:
            self.license = None
        elif license is not None:
            self.license = license
        else:
            raise Exception("Employee must have license")
        self.phone = phone
        self.interest_rate = interest_rate
        self.salary = salary


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
            