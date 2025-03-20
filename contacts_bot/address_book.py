from collections import UserDict
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from models import Record

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
                    "birthday": this_year_birthday.strftime("%d.%m.%Y"),
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
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