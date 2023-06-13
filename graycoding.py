from typing import List

# TODO: Recursion is (maybe) not the best way to do this?
def gray_code(bits: int) -> List[int]:
    if bits == 1:
        return [0, 1]
    else:
        prev = gray_code(bits - 1)
        return [0 + i for i in prev] + [1 + i for i in prev[::-1]]

# Test gray_code()
print(gray_code(8))
