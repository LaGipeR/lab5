from sys import argv
import json
import re
import datetime


def load(info, csv_name, json_name, encoding):
    print(f"input-csv {csv_name}:", end=" ")
    load_csv(info, csv_name, encoding)
    print("OK")

    print(f"input-json {json_name}:", end=" ")
    add_info = load_json(json_name, encoding)
    print("OK")

    print("json?=csv:", end=" ")
    print("OK" if check(info, add_info) else "UPS")


def load_csv(info, csv_name, encoding):
    info.clear()


def load_json(json_name, encoding):
    with open(json_name, 'r', encoding=encoding) as file:
        add_info = json.load(file)

        if "загальна кількість записів" not in add_info:
            raise ValueError("No key 'загальна кількість записів' in json")
        if "кількість «не з'явився»" not in add_info:
            raise ValueError("No key 'кількість «не з'явився»' in json")

        return [add_info["загальна кількість записів"], add_info["кількість «не з'явився»"]]


def check(info, add_info):
    return True


class Info:
    def __init__(self):
        self.tasks = []
        self.cnt = 0
        self.min_year = 9999

    def clear(self):
        self.tasks = []
        self.cnt = 0
        self.min_year = 9999

    def output(self, out_name, encoding):
        with open(out_name, "w", encoding=encoding) as file:
            for task in self.tasks:
                if not 60 <= task.get_min() and task.get_max() <= 90:
                    continue

                file.write(f"{task.get_attempts()}\t{task.get_average():}\t{task.get_u()}\n")
                task.output(file)

    def load(self, name, surname, day, month, year, mark, u):
        # Знайти задачу по умові (u)
        # якщо нема до додає задачу з умовою u
        # додаємо спробу до задачі
        # оновлює найменший рік спроби, та кількість спроб

        task = self.find(u)
        if task is None:
            task = self.add(u)

        task.load(name, surname, day, month, year, mark)

        self.min_year = min(self.min_year, year)
        self.cnt += 1

    def find(self, u):
        for task in self.tasks:
            if task.u == u:
                return task
        return None

    def add(self, u):
        new_task = Task(u)
        self.tasks.append(new_task)
        return new_task


class Task:
    def __init__(self, u):
        if not re.fullmatch(r"[-\w\"\d .,{}$+*()%\[\]]{3,55}", u):
            raise Exception
        self.u = u

        self.tries = []
        self.max = 0
        self.min = 0
        self.sum = 0

    def output(self, file):
        self.tries.sort()

        for attempt in self.tries:
            file.write(f"\t{attempt.get_second_name()}\t{attempt.get_first_name()}\t{attempt.get_mark()}\n")

    def get_average(self):
        return self.sum / self.get_cnt()

    def get_cnt(self):
        return len(self.tries)

    def load(self, name, surname, day, month, year, mark):
        # створює нову спробу
        # додає її до списку спроб
        # оновляє мінімальну і максимальну оцінку
        # оновляє суму, щоб порахувати середню оцінку
        self.add(name, surname, day, month, year, mark)

        self.min = min(self.min, mark)
        self.max = max(self.max, mark)

        self.sum += mark

    def add(self, name, surname, day, month, year, mark):
        new_try = Try(name, surname, day, month, year, mark)
        self.tries.append(new_try)
        return new_try


class Try:
    def __init__(self, name, surname, day, month, year, mark):
        if not isinstance(mark, int) and 0 <= mark <= 100:
            raise Exception
        self.mark = mark

        if not isinstance(surname, str) and re.fullmatch(r"[-\w' ]{1,30}", surname):
            raise Exception
        self.surname = surname

        if not isinstance(name, str) and re.fullmatch(r"[-\w' ]{1,26}", name):
            raise Exception
        self.name = name

        if not isinstance(year, int) and year >= 2001 and datetime.date(year, month, day):
            raise Exception
        self.day = 0
        self.month = 0
        self.year = 0

    def get_mark(self):
        return self.mark

    def get_surname(self):
        return self.surname

    def get_name(self):
        return self.name

    def get_day(self):
        return self.day

    def get_month(self):
        return self.month

    def get_year(self):
        return self.year

    def __lt__(self, other):
        return (self.get_surname(), self.get_name(), -self.get_mark()) < \
               (other.get_surname(), other.get_name(), -other.get_mark())







def ini_load(p):
    with open(p, "r", encoding="utf-8") as file:
        options = json.load(file)

        if "input" not in options:
            raise Exception("No key 'input'")
        if "output" not in options:
            raise Exception("No key 'output'")

        if "json" not in options["input"]:
            raise Exception("No key 'json' in key 'input'")
        if "csv" not in options["input"]:
            raise Exception("No key 'csv' in key 'input'")
        if "encoding" not in options["input"]:
            raise Exception("No key 'encoding' in key 'input'")

        if "fname" not in options["output"]:
            raise Exception("No key 'fname' in key 'output'")
        if "encoding" not in options["output"]:
            raise Exception("No key 'encoding' in key 'output'")

        return options


def process(p):
    try:
        print(f"ini {p}:", end=" ")
        setting = ini_load(p)
        print("OK")

        info = Info()
        load(info, setting["input"]["csv"], setting["input"]["json"], setting["input"]["encoding"])

        info.output()

    except BaseException as e:
        print("\n***** program aborted *****")
        print(e)


if __name__ == '__main__':
    print("*****")

    if len(argv) == 2:
        ini_path = argv[1]
        process(ini_path)
    else:
        print("***** program aborted *****")


"""
ім'я        - Спроба name       str [1, 26]
прізвіще    - Спроба surname    str [1, 30]

день        - Спроба day        int [1, 31]
місяць      - Спроба month      int [1, 12]
рік         - Спроба year       int [2001; ...]

бали        - Спроба mark       int [0; 100]

умова       - Задача task       str [3; 55]
---------
найменший рік       - Інформація
кільсть спроб       - Інформація
---------

мінімальну оцінку   - Задача
максимальну оцінку  - Задача

кількість спроб             - Задача
середня розв'язуваність     - Задача



60 <= min <= all <= max <= 90
1     100     1
60 <=        all        <= 90

"""
