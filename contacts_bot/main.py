from address_book import AddressBook
from utils import parse_input
from handlers import (
    handle_add_contact,
    handle_change_contact,
    handle_show_phone,
    handle_show_all,
    handle_add_birthday,
    handle_show_birthday,
    handle_birthdays
)

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
            print(handle_birthdays(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
