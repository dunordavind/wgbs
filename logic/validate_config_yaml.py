import os
import re

from structures.mate_handler import MateHandler


def validate_config_yaml(args):
    mate_handler = MateHandler()
    validate_all_mates_exist(mate_handler)
    check_number_of_samples(mate_handler)
    check_duplicated_mate_names(mate_handler)
    verify_naming_pattern(mate_handler)


def validate_all_mates_exist(mate_handler):
    messages = []
    for mate in mate_handler.list_project_mates():
        if not os.path.isfile(mate.first):
            messages.append("File " + mate.first + " for mate " + mate.name + " does not exist")
        if not os.path.isfile(mate.second):
            messages.append("File " + mate.second + "for mate " + mate.name + " does not exist")
    for message in messages:
        print(message)


def check_duplicated_mate_names(mate_handler):
    ##check if any mate files are duplicated
    seen = set()
    duplicates = []
    for mate_file in mate_handler.list_all_mate_files():
        if mate_file in seen:
            duplicates.append(mate_file)
        else:
            seen.add(mate_file)
    if len(duplicates) != 0:
        print("The following files are duplicated:")
        for duplicate in duplicates:
            print(duplicate)
    else:
        print("No duplicates found")


def check_number_of_samples(mate_handler):
    ##check how many mates in samples there are
    for sample in mate_handler.list_samples():
        print("Sample " + sample.name + " contains " + str(len(sample.mates)) + " mates ")


def verify_naming_pattern(mate_handler):
    for mate in mate_handler.list_project_mates():
        suspicious = False
        if os.path.dirname(mate.first) != os.path.dirname(mate.second):
            suspicious = True

        first_name = os.path.basename(mate.first)
        second_name = os.path.basename(mate.second)

        first_res = re.match("(.*)_R1_(.*)", first_name)
        second_res = re.match("(.*)_R2_(.*)", second_name)

        if first_res and second_res:
            if first_res.group(1) != second_res.group(1) or first_res.group(2) != second_res.group(2):
                suspicious = True
        else:
            suspicious = True

        if suspicious:
            print("This mate looks suspicious:")
            print(mate.name)
            print(mate.first)
            print(mate.second)