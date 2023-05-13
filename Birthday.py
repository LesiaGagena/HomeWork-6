import datetime

class Field:
    def __init__(self, value=None):
        self.__value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{type(self).__name__}(value={self.value!r})"

    def validate(self, value):
        return True

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if self.validate(value):
            self.__value = value
        else:
            raise ValueError(f"Invalid value {value} for {type(self).__name__}")

class Phone(Field):
    def validate(self, value):
        return isinstance(value, str) and all(char.isdigit() for char in value)

    @property
    def value(self):
        return f"+{self.__value}"

    @value.setter
    def value(self, value):
        if self.validate(value):
            self.__value = value
        else:
            raise ValueError(f"Invalid phone number {value}")

class Birthday(Field):
    def validate(self, value):
        if isinstance(value, str):
            try:
                datetime.datetime.strptime(value, '%d.%m.%Y')
                return True
            except ValueError:
                pass
        return False

    @property
    def value(self):
        return datetime.datetime.strptime(self.__value, '%d.%m.%Y').date()

    @value.setter
    def value(self, value):
        if self.validate(value):
            self.__value = value
        else:
            raise ValueError(f"Invalid birthday date {value}")

class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = Field(name)
        self.phone = Phone(phone)
        self.birthday = Birthday(birthday) if birthday else None

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.date.today()
            this_year_birthday = datetime.date(today.year, self.birthday.value.month, self.birthday.value.day)
            if this_year_birthday < today:
                this_year_birthday = datetime.date(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            days_to_birthday = (this_year_birthday - today).days
            return days_to_birthday

    def __str__(self):
        return f"{self.name.value} ({self.phone.value}), {self.birthday.value}" if self.birthday else f"{self.name.value} ({self.phone.value})"

class AddressBook:
    def __init__(self):
        self.__records = []

    def add_record(self, record):
        self.__records.append(record)

    def delete_record(self, record):
        self.__records.remove(record)

    def iterator(self, page_size=10):
        page = 0
        while True:
            start_index = page * page_size
            end_index = start_index + page_size
            current_page = self.__records[start_index:end_index]
            if not current_page:
                break
            yield current_page
            page += 1
