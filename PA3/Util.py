import csv
import re

def get_transactions(filename):
    with open(filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        result = []
        for row in csv_reader:
            row_result = []
            for item in row:
                item = replace_non_ascii_with_space(item)
                item = item.strip('\n').strip('\r')
                row_result.append(item)
            result.append(row_result)
    return result

def replace_non_ascii_with_space(input_doc):
    return re.sub(r'[^\x00-\x7F]+', ' ', input_doc)

if __name__ == "__main__":
    print get_dataset('NYC_Wi-Fi_Hotspot_Locations_Map.csv')[:10]
