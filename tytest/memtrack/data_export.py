import csv
import os
import json

from .constants import BEFORE_CPU, AFTER_CPU, BEFORE_MEMORY_TOTAL, AFTER_MEMORY_TOTAL, BEFORE_MEMORY_PERCENT, \
    AFTER_MEMORY_PERCENT, PROCESS_NAME, PID, STARTED_AT, FINISHED_AT, PROCESSES, TEST_NAME, TEST

__parameters = [BEFORE_CPU, BEFORE_MEMORY_TOTAL, BEFORE_MEMORY_PERCENT,
                AFTER_CPU, AFTER_MEMORY_TOTAL, AFTER_MEMORY_PERCENT]


def prepare_consumption_data_for_export(data):
    for test in data.keys():
        for pid, process in data[test][PROCESSES].items():
            for parameter in __parameters:
                if parameter not in process:
                    process[parameter] = 0.0


def export_consumption_data(export_directory, data, formats):
    for data_format in formats:
        if data_format == "csv":
            __export_as_csv(export_directory, data)
        elif data_format == "tsv":
            __export_as_tsv(export_directory, data)
        elif data_format == "json":
            __export_as_json(export_directory, data)


def __export_as_csv(export_directory, data):
    __export_as_sv(",", "csv", export_directory, data)
    print("Resource consumption data exported in csv file.")


def __export_as_tsv(export_directory, data):
    __export_as_sv("\t", "tsv", export_directory, data)
    print("Resource consumption data exported in tsv file.")


def __export_as_sv(delimiter, data_format, export_directory, data):
    header = [TEST_NAME, STARTED_AT, FINISHED_AT, PID, PROCESS_NAME, PROCESS_NAME] + __parameters
    rows = [{**{TEST_NAME: test, STARTED_AT: test_data[STARTED_AT], FINISHED_AT: test_data[FINISHED_AT],
                PID: pid, PROCESS_NAME: process_data[PROCESS_NAME]}, **process_data}
            for test, test_data in data.items() for pid, process_data in test_data[PROCESSES].items()]

    file_path = os.path.join(export_directory,
                             'resources.{}'.format(data_format))
    with open(file_path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(rows)


def __export_as_json(export_directory, data):
    result_data = []
    for test, test_info in data.items():
        test_data = {TEST: test, STARTED_AT: test_info[STARTED_AT], FINISHED_AT: test_info[FINISHED_AT], PROCESSES: []}
        for pid, process in test_info[PROCESSES].items():
            test_data[PROCESSES].append({**{PID: pid}, **process})
        result_data.append(test_data)

    file_path = os.path.join(export_directory, "resources.json")
    with open(file_path, "w", encoding="UTF8", newline="") as f:
        f.write(json.dumps(result_data, indent=4))
    print("Resource consumption data exported in json file.")
