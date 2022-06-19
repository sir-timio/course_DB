from datetime import datetime
import json

class Entity:
    def __init__(self) -> None:
        pass
    
    def get_data(self):
        return dict((k, v) for k, v in self.__dict__.items() if v is not None)

from enum import Enum
class Specialization(Enum):
    ADMINISTRATOR = 1
    NURSE = 2
    DOCTOR = 3

    def __str__(self):
        return self.name

   
class Stuff(Entity):
    def __init__(
        self,
        specialization: Specialization,
        name: str,
        surname: str,
        id: int = None,
        license: str = None,
        phone: str = None,
        birth_date: datetime = None,
        interest_rate: float = None,
        salary: int = None
    ) -> None:

        super().__init__()
        self.id = id
        self.name = name
        self.surname = surname
        self.specialization = specialization.value

        if self.specialization in [Specialization.ADMINISTRATOR.value]:
            self.license = None
        elif license is not None:
            self.license = license
        else:
            raise Exception("Employee must have license")
        self.phone = phone
        self.birth_date = birth_date
        self.interest_rate = interest_rate
        self.salary = salary

    
            