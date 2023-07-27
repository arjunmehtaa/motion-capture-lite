from location import get_relative_location

# should print outputs from 0-7 inclusive, this is for 3 bits
print(get_relative_location([0,0,0], 0, 0, 7, True))
print(get_relative_location([0,0,1], 0, 0, 7, True))
print(get_relative_location([0,1,1], 0, 0, 7, True))
print(get_relative_location([0,1,0], 0, 0, 7, True))
print(get_relative_location([1,1,0], 0, 0, 7, True))
print(get_relative_location([1,1,1], 0, 0, 7, True))
print(get_relative_location([1,0,1], 0, 0, 7, True))
print(get_relative_location([1,0,0], 0, 0, 7, True))