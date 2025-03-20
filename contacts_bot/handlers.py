from typing import List
from utils import input_error
from address_book import AddressBook

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
def handle_birthdays(book: "AddressBook") -> str:
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