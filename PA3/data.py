import sys
from csv import reader, writer

from itertools import combinations, permutations

count_range = 50
percent_range = 20


def data_normalize(filename):
    output = file('integrated.csv', 'w')
    is_csv_field = True
    with open(filename, 'r') as csvfile:        
        csv_reader = reader(csvfile, delimiter=',')
        csv_writer = writer(output, dialect='excel')
        for row in csv_reader:
            if not is_csv_field:
                for i in xrange(len(row)):
                    if i == 4:
                       count = int(row[i])
                       range_flag = count / count_range
                       row[i] = str(count_range * range_flag) + ' -> ' + str(count_range * (range_flag + 1) - 1)
                    if i == 5:
                       percent = int(row[i])
                       range_flag = percent / percent_range
                       row[i] = str(percent_range * range_flag) + ' -> ' + str(percent_range * (range_flag + 1) - 1)
            csv_writer.writerow(row)
            is_csv_field = False
    output.close()

def data_split(filename):
    output = file('splitted.csv', 'w')
    is_csv_field = True
    count_idx = 4
    with open(filename, 'r') as csvfile:        
        csv_reader = reader(csvfile, delimiter=',')
        csv_writer = writer(output, dialect='excel')
        for row in csv_reader:
            if is_csv_field:
                csv_writer.writerow(row)
                is_csv_field = False
            else:
                if row[count_idx] == '.':
                    row[count_idx] = '0'
                count = int(row[count_idx])
                while count:
                    csv_writer.writerow(row[:count_idx] + row[count_idx + 1:])
                    count -= 1
    output.close()

def test_splitted_data(filename):
    with open(filename, 'r') as csvfile:        
        csv_reader = reader(csvfile, delimiter=',')
        total_row_num = 6
        for row in csv_reader:
            if len(row) != total_row_num:
                print row
                break
    print "All rows are valid!"

def data_modify(filename):
    output = file('modified.csv', 'w')
    with open(filename, 'rU') as csvfile:        
        csv_reader = reader(csvfile, dialect='excel', delimiter=',')
        csv_writer = writer(output, dialect='excel')
        for row in csv_reader:
            if "Pulse/Heart Rate" in row:
                row[row.index("Pulse/Heart Rate")] = "Pulse-Heart Rate"
            csv_writer.writerow(row)
    output.close()

                
if __name__ == "__main__":
    # data_normalize(sys.argv[1])
    data_split(sys.argv[1])
    # test_splitted_data(sys.argv[1])
    # data_modify(sys.argv[1])
