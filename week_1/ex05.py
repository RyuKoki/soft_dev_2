# ex05.py

def triplet_zero(array):

    carry = []

    for i in range(len(array)-1):
        for j in range(i+1, len(array)):
            carry.append([array[i], array[j]])
    
    for k in range(len(carry)):
        index_last = array.index(carry[k][1])
        # print(array[index_last+1:])
        first_term = carry[k][0]
        mid_term = carry[k][1]
        last_term = array[index_last+1:]
        for m in range(len(last_term)):
            total = first_term + mid_term + last_term[m]
            if ( total == 0 ):
                print("{}, {}, {}".format(first_term, mid_term, last_term[m]))


a = [0, -1, 2, -3, 1, -2]
triplet_zero(a)   # output >> (0, -1, 1), (0, 2, -2), (2, -3, 1)
