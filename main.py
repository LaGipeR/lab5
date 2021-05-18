"""
Виконавець: такий то
Варінт: 65
Задача: така то
"""

from sys import argv
import json
from load import load


def load_ini(p):
    with open(p, "r") as ini_file:
        settings = json.load(ini_file)

        if "input" not in settings or "output" not in settings:
            raise ValueError("Not found keys 'input' or 'output' in csv")

        in_settings = settings["input"]
        if "json" not in in_settings or "csv" not in in_settings or "encoding" not in in_settings:
            raise ValueError("Not found keys 'json' or 'csv' or encoding in csv['input']")

        out_settings = settings["output"]
        if "fname" not in out_settings or "encoding" not in out_settings:
            raise ValueError("Not found keys 'fname' or 'encoding' in csv['output']")

        return settings


def main(p):
    try:
        print(f"ini {p}:", end=" ")
        settings = load_ini(p)
        print("OK")

        info = load(settings["input"]["csv"], settings["input"]["json"], settings["input"]["encoding"])

        print(f"output {settings['output']['fname']}:", end=" ")
        info.output(settings["output"]["fname"], settings["output"]["encoding"])
        print("OK")

    except Exception as e:
        print("\n***** program aborted *****")
        print(e)


print("WARNING: Сумарна оцінка в балах та за державною шкалою, узгоджені між собою. Don't do")
print("WARNING: Якщо на екзамені набрані бали рівні 0, то оцінка не може бути задовільною. Do")
if __name__ == '__main__':
    print(__doc__)
    print("*****")

    if len(argv) == 2:
        main(argv[1])
    else:
        print("***** program aborted *****")
