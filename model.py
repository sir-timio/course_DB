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


class Patient(Entity):
    def __init__(
        self,
        id: int,
        name: str,
        surname: str,
        phone: str = None,
    ) -> None:

        super().__init__()
        self.id = int(id)
        self.name = str(name)
        self.surname = str(surname) if surname is not None else ''
        self.phone = str(phone) if phone is not None else ''

    def get_name(self):
        return f'{self.id} {self.name}{" " * bool(len(self.surname) > 0) + self.surname}'
    

class Treatment (Entity):
    def __init__(
        self,
        id: int,
        visit_id: int,
        code: int,
        location: int,
        quantity: int,
    ) -> None:

        super().__init__()
        self.id = int(id)
        self.visit_id = int(visit_id)
        self.code = int(code)
        self.location = int(location)
        self.quntity = int(quantity)

class Price_list(Entity):
    def __init__(
        self,
        code: int,
        name: str,
        price: float
    ) -> None:

        super().__init__()
        self.code = int(code)
        self.name = str(name)
        self.price = float(price)
    
    def get_name(self, code_to_name: dict):
        return code_to_name[self.code]

