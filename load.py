import csv

from classes import Info
import json


def load(csv_name, json_name, encoding):
    info = Info()
    print(f"input-csv {csv_name}:", end=" ")
    load_data(info, csv_name, encoding)
    print("OK")

    print(f"input-json {json_name}:", end=" ")
    add_info = load_json(json_name, encoding)
    print("OK")

    print("json?=csv:", end=" ")
    print("OK" if check(info, add_info) else "UPS")

    return info


def load_data(info: Info, csv_name: str, encoding: str):
    info.clear()

    with open(csv_name, "r", encoding=encoding) as file:
        reader = csv.reader(file, delimiter=';')

        for line in reader:
            if len(line) == 0:
                continue

            if len(line) != 10:
                raise Exception

            subject_name = line[0]
            middle_name = line[1]
            exam_mark = int(line[2])
            mark = int(line[3])
            second_name = line[4]
            group = line[5]
            semester_mark = int(line[6])
            first_name = line[7]
            number = line[8]
            sum_mark = int(line[9])

            info.load(first_name, middle_name, second_name, group, number,
                      subject_name, exam_mark, mark, semester_mark, sum_mark)


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
