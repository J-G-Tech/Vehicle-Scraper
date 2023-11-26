def format_list(my_list):
    list_final = my_list[::2] 
    first_strings = ", ".join(list_final)
    return first_strings + " and " + my_list[-1]


def shift_left(my_list): 
    return my_list[1::] + [my_list[0]]

def extend_list(list_x, list_y):
    list_y[len(list_y):] = list_x
    return list_y

list_y = [0,1,2,3]
list_x = [4,5,6]
my_list = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday"]
print(extend_list(list_x,list_y ))
