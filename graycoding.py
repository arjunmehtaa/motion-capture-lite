from typing import List

# TODO: Recursion is (maybe) not the best way to do this?
def gray_code(bits: int) -> List[str]:
    if bits == 1:
        return ["0", "1"]
    else:
        codes = gray_code(bits - 1)
        return ["0" + code for code in codes] + ["1" + code for code in codes[::-1]]

# Test gray_code()
print(gray_code(8))
