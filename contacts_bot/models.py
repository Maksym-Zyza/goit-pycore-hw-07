from typing import List, Optional
from datetime import datetime


class ValidationException(Exception):
    pass


class Field:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value)
        self.validate_name(value)

    def validate_name(self, value: str) -> None:
        if not value.isalpha():
            raise ValidationException("Name must contain only letters")


class Phone(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value)
        self.validate_phone(value)

    def validate_phone(self, value: str) -> None:
        if not value.isdigit() or len(value) != 10:
            raise ValidationException("Phone number must be 10 digits")


class Birthday(Field):
    def __init__(self, value: str) -> None:
        try:
            self.value: datetime.date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValidationException("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name: str) -> None:
        self.name: Name = Name(name)
        self.phones: List[Phone] = []
        self.birthday: Optional[Birthday] = None
        
    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return
        raise ValidationException("Phone number not found")
    
    def find_phone(self, phone: str) -> Optional[Phone]:
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    def remove_phone(self, phone: str) -> None:
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValidationException("Phone number not found")

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)
        
    def show_birthday(self) -> str:
        return self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "Birthday not set"

    def __str__(self) -> str:
        birthday_str = f", birthday: {self.show_birthday()}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{birthday_str}"