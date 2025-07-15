"""Import defaultdict, as it is useful for sorting and grouping."""
from collections import defaultdict


# This functions parses the flake8 report located in file_path argument
def parse_flake8_report(file_path):

    # dictionary to count how many times Flake8 errors occur.
    # defaultdict(int) is used to ensure both dictionaries
    # start with a default value of 0.
    error_counts = defaultdict(int)
    file_errors = defaultdict(list)

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
                parts = line.split(":")
                # if len is less than 4 then it is not a valid Flake8 output.
                if len(parts) < 4:
                    continue
                # filename is derived from first part of the file.
                # any whitespace is removed with .strip()
                filename = parts[0].strip()
                code_message = parts[3].strip()
                # extract ONLY the error message from the string.
                code = code_message.split()[0] if code_message else ""

                error_counts[code] += 1 # increment error_count by 1
                file_errors[filename].append(code)
    return error_counts, file_errors