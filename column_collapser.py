#!/usr/bin/python
import sys
import csv
import re

class ColumnCollapser:
    SAFE_PRINT_FILTER_PATTERNS = [
        # insert any regex patterns you want replaced in the output (ssn / credit card / etc)
        r"column-collapser isn't the coolest tool",
    ]

    @classmethod
    def _safe_print(cls, content):
        safe_content = content
        for pattern in cls.SAFE_PRINT_FILTER_PATTERNS:
            safe_content = re.sub(pattern,"[COLLAPSER-FILTERED]", str(content))
        print(safe_content)

    @classmethod
    def _handle(cls, header, index, row):
        header = header if header is not None else "N/A"
        return "{:25s} {:4s}: {}".format(header, index, row)

    @classmethod
    def _prompt_merge_columns(cls, headers, row):
        indexes = [ "[{}]".format(i) for i in range(0, len(row))]

        for message in map(cls._handle, headers, indexes, row):
            cls._safe_print(message)

        try:
            merge_response = raw_input("Which columns would you like to merge (e.g. '1 2')? ").strip()
            merge_indexes = [ int(i) for i in merge_response.split(" ") ]

            new_value = " ".join([row[index] for index in merge_indexes])
            target = merge_indexes.pop(0)

            row[target] = new_value
            for index in merge_indexes:
                row.pop(index)

        except (IndexError, ValueError) as e:
            cls._safe_print("Error in input: {}".format(e))

    @classmethod
    def fixup_lines(cls, filename):
        with open(filename, 'r') as reader_object:
            with open(filename+'.collapsed_output','w') as writer_object:
                reader = csv.reader(reader_object)
                writer = csv.writer(writer_object)
                headers = reader.next()
                writer.writerow(headers)
                for row in reader:
                    while len(row) > len(headers):
                        cls._prompt_merge_columns(headers, row)

                    writer.writerow(row)

if __name__ == "__main__":
    if not len(sys.argv) == 2:
        print("usage: python digest.py file_with_too_many_commas")
        exit(1)

    ColumnCollapser.fixup_lines(filename=sys.argv[1])
