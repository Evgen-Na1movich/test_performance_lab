import json
import sys


def fill_values(tests, values):
    for test in tests:
        for value in values['values']:
            if test['id'] == value['id']:
                test['value'] = value['value']
        if 'values' in test:
            fill_values(test['values'], values)   #рекурсивный вызов функции
    return tests


def main(values_path, tests_path, report_path):
    with open(values_path, 'r') as values_file:
        values_data = json.load(values_file)  # считываем данные из файла

    with open(tests_path, 'r') as tests_file:
        tests_data = json.load(tests_file)  # считываем данные из файла

    fill_values(tests_data['tests'], values_data)

    with open(report_path, 'w') as report_file:
        json.dump(tests_data, report_file, indent=2)


if __name__ == '__main__':
    # values_file = sys.argv[1]
    # tests_file = sys.argv[2]
    # report_file = sys.argv[3]
    values_file = 'values.json'
    tests_file = 'tests.json'
    report_file = 'report.json'


    main(values_file, tests_file, report_file)
