from location import get_region

# should print outputs from 0-7 inclusive, this is for 3 bits
print(get_region([0,0,0], 0, 0, 7, True))
print(get_region([0,0,1], 0, 0, 7, True))
print(get_region([0,1,1], 0, 0, 7, True))
print(get_region([0,1,0], 0, 0, 7, True))
print(get_region([1,1,0], 0, 0, 7, True))
print(get_region([1,1,1], 0, 0, 7, True))
print(get_region([1,0,1], 0, 0, 7, True))
print(get_region([1,0,0], 0, 0, 7, True))