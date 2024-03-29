def cast(var, cls):
    if var is not None:
        return cls(var)
    return None

class Entity:
    def __init__(self) -> None:
        pass
    
    def get_data(self):
        return dict((k, v) for k, v in self.__dict__.items() if v is not None)

from enum import Enum
class Job(Entity):
    def __init__(
        self,
        id: int,
        job_name: str,
        daily_salary: float,
    ) -> None:

        super().__init__()
        self.id = cast(id, int)
        self.daily_salary = cast(daily_salary, float)
        self.name = cast(job_name, str)
    
    def get_name(self):
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
        name: str,
        surname: str,
        phone: str,
        job_id: int,
        license: str = None,
        interest_rate: float = None,
    ) -> None:

        super().__init__()
        self.id = cast(id, int)
        self.name = cast(name, str)
        self.surname = cast(surname, str)
        self.job_id = cast(job_id, int)

        self.license = cast(license, str)
        self.phone = cast(phone, str)
        self.interest_rate = cast(interest_rate, float)

    def get_name(self, job: dict = None):
        if job is not None:
            return f'{job[self.job_id].name} {self.name} {self.surname}'
        return f'{self.name} {self.surname}'
    def is_doctor(self):
        return self.job_id == 3


class Qualification(Entity):
    def __init__(
        self,
        id: int,
        specialization: Specialization,
        organization: str,
        stuff_id: int,
        date: str = None,
        description: str = None,
    ) -> None:

        super().__init__()
        self.id = cast(id, int)
        self.specialization = specialization.value
        self.organization = cast(organization, str)
        self.stuff_id = cast(stuff_id, int)
        self.date = cast(date, str)
        self.description = cast(description, str)


class Visit(Entity):
    def __init__(
        self,
        patient_id: int,
        doctor_id: int,
        date: str = None,
        time: str = None,
        room: int = None,
        receipt: str = None,
    ) -> None:
        super().__init__()
        self.patient_id = cast(patient_id, int)
        self.doctor_id = cast(doctor_id, int)
        self.date = cast(date, str)
        self.time = cast(time, str)
        self.room = cast(room, int)
        self.receipt = cast(receipt, str)


class Patient(Entity):
    def __init__(
        self,
        id: int,
        name: str,
        surname: str,
        phone: str = None,
    ) -> None:

        super().__init__()
        self.id = cast(id, int)
        self.name = cast(name, str)
        self.surname = cast(surname, str)
        self.phone = cast(phone, str)

    def get_name(self):
        return f'{self.name}{" " * bool(len(self.surname) > 0) + self.surname}'
    

class MedicalCart(Entity):
    def __init__(
        self,
        id: int,
        sex: str,
        blood_type: str,
        birth_date: str,
        allergy: str,
        diseases: str,
        medicines: str,
    ) -> None:
        super().__init__()
        self.id = cast(id, int)
        self.sex = cast(sex, str)
        self.blood_type = cast(blood_type, str)
        self.birth_date = cast(birth_date, str)
        self.allergy = cast(allergy, str)
        self.diseases = cast(diseases, str)
        self.medicines = cast(medicines, str)


class Treatment (Entity):
    def __init__(
        self,
        id: int,
        visit_id: int,
        price_list_id: int,
        location: int,
        quantity: int,
    ) -> None:

        super().__init__()
        self.id = cast(id, int) 
        self.visit_id = cast(visit_id, int)
        self.price_list_id = cast(price_list_id, int)
        self.location = cast(location, int)
        self.quantity = cast(quantity, int)

class Workdays(Entity):
    def __init__(
        self,
        stuff_id: int,
        date: str,
        id: int = None,
    )-> None:

        super().__init__()
        self.id = cast(id, int)
        self.stuff_id = cast(stuff_id, int)
        self.date = cast(date, str)
    
    def get_day_code(self, s):
        if s == 'пн':
            return '1'
        elif s == 'вт':
            return '2'
        elif s == 'ср':
            return '3'
        elif s == 'чт':
            return '4'
        elif s == 'пт':
            return '5'
        elif s == 'сб':
            return '6'
        elif s == 'вс':
            return '0'
        else:
            raise('Unknown weekdate')

class Price_list(Entity):
    def __init__(
        self,
        id: int,
        name: str,
        price: float
    ) -> None:

        super().__init__()
        self.id = int(id)
        self.name = str(name)
        self.price = float(price)
    
    def get_name(self, code_to_name: dict):
        return code_to_name[self.code]

