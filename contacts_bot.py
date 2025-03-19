from typing import Callable, List, Dict, Tuple, Optional, Any
from collections import UserDict
from datetime import datetime, timedelta


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


class AddressBook(UserDict):
    def add_record(self, record: "Record") -> None:
        self.data[record.name.value] = record
    
    def find(self, name: str) -> Optional["Record"]:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self) -> List[Dict[str, str]]:
        today = datetime.now().date()
        upcoming_birthdays = []
        
        for record in self.data.values():
            if not record.birthday:
                continue

            birthday = record.birthday.value            
            this_year_birthday = birthday.replace(year=today.year)

            if this_year_birthday < today:
                this_year_birthday = this_year_birthday.replace(year=today.year + 1)

            if 0 <= (this_year_birthday - today).days <= 7:
                congratulation_date = this_year_birthday

                if congratulation_date.weekday() == 5:  # Saturday
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:  # Sunday
                    congratulation_date += timedelta(days=1)

                upcoming_birthdays.append({
                    "name": record.name.value,
                    "birthday": congratulation_date.strftime("%d.%m.%Y"),
                    "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
                })
                
        return upcoming_birthdays

    def add_contact(self, name: str, phone: Optional[str] = None) -> str:
        record = self.find(name)
        if record is None:
            record = Record(name)
            self.add_record(record)
            message = "Contact added."
        else:
            message = "Contact updated."
        if phone:
            record.add_phone(phone)
        return message

    def change_contact(self, name: str, old_phone: str, new_phone: str) -> str:
        record = self.find(name)
        if record is None:
            raise KeyError('Contact not found.')
        record.edit_phone(old_phone, new_phone)
        return "Phone number updated."

    def show_phone(self, name: str) -> str:
        record = self.find(name)
        if record is None:
            raise KeyError('Contact not found.')
        return '; '.join(phone.value for phone in record.phones)

    def show_all(self) -> str:
        if not self.data:
            return "No contacts available."
        return '\n'.join(str(record) for record in self.data.values())


def input_error(func: Callable[..., Any]) -> Callable[..., Any]:
    def inner(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)
    return inner


@input_error
def handle_add_birthday(args: List[str], book: "AddressBook") -> str:
    if len(args) != 2:
        raise IndexError("Please provide contact name and birthday date.")
    
    name, date = args
    record = book.find(name)
    if not record:
        raise KeyError("Contact not found.")
    record.add_birthday(date)
    return "Birthday added"


@input_error
def handle_show_birthday(args: List[str], book: "AddressBook") -> str:
    if len(args) != 1:
        raise IndexError("Please provide contact name.")
    
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError("Contact not found.")
    return record.show_birthday()


@input_error
def handle_birthdays(args: List[str], book: "AddressBook") -> str:
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "There are no birthdays in the next 7 days."
    
    result = [
        f"{b['name']}: birthday on {b['birthday']}, celebrate on {b['congratulation_date']}"
        for b in upcoming
    ]
    return "\n".join(result)


@input_error
def handle_add_contact(args: List[str], book: "AddressBook") -> str:
    if len(args) != 2:
        raise IndexError("Please provide contact name and phone number.")
    
    name, phone = args
    return book.add_contact(name, phone)


@input_error
def handle_change_contact(args: List[str], book: "AddressBook") -> str:
    if len(args) != 3:
        raise IndexError("Please provide contact name, old phone number and new phone number.")
    
    name, old_phone, new_phone = args
    return book.change_contact(name, old_phone, new_phone)


@input_error
def handle_show_phone(args: List[str], book: "AddressBook") -> str:
    if len(args) != 1:
        raise IndexError("Please provide contact name.")
    
    name = args[0]
    return book.show_phone(name)


@input_error
def handle_show_all(book: "AddressBook") -> str:
    return book.show_all()


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    if not user_input.strip():
        return "", []
    
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    args = [arg.strip() for arg in args]
    return cmd, args


def main() -> None:
    book = AddressBook()
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if not command:
            print("Please enter a command")
            continue

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(handle_add_contact(args, book))
        elif command == "change":
            print(handle_change_contact(args, book))
        elif command == "phone":
            print(handle_show_phone(args, book))
        elif command == "all":
            print(handle_show_all(book))
        elif command == "add-birthday":
            print(handle_add_birthday(args, book))
        elif command == "show-birthday":
            print(handle_show_birthday(args, book))
        elif command == "birthdays":
            print(handle_birthdays(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
