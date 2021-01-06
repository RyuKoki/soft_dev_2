# ex04.py

def read_csv(file_name):

    # This function's for reading .csv file

    import csv

    row_item = [] # storing all of rows
    
    with open('{}'.format(file_name)) as data:
        reader = csv.reader(data)

        for row in reader:
            # print(row)
            for ele in range(len(row)):
                row[ele] = int(row[ele]) # casting str() --> int()

            row_item.append(row) # save all rows

    result = row_item.copy()

    for r in range(len(row_item)):
        result.append([item[r] for item in row_item]) # for getting all columns' lists

    # print(get_item)
    return result

# test_table = read_csv('mixed_ten.csv')
# print(test_table)


def mixed_ten(file):

    table = read_csv('{}'.format(file))
    # print(table)
    most_term = int(len(table)/2)
    num_term = most_term

    answer = 0

    # This loop's for all of rows
    while ( num_term >= 2 ):
        for x in range(len(table)): # access each list in list
            if ( num_term == most_term ): # all elements are adds themselves
                total = sum( table[x] )
                if ( total == 10 ):
                    answer += 1
                    print(table[x])

            else:
                for y in range(most_term-num_term+1): # access each element in row
                    total = sum( table[x][y:num_term+y] )
                    if ( total == 10 ):
                        answer += 1
                        print(table[x][y:num_term+y])

        num_term -= 1

    print(answer)

mixed_ten('mixed_ten.csv')
