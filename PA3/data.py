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
                
if __name__ == "__main__":
    data_normalize(sys.argv[1])
    # you are a fucking asshole. why do you care their problem! stupid girl?!!! go to hell!    
    # The guy will be deadddddddddd.