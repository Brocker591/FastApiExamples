from typing import Union, Optional

def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    return a + b



def add_with_default(a: Union[int, float], b: Union[int, float], c: Optional[Union[int, float]] = None) -> Union[int, float]:
    if not c:
        return a + b
    return a + b + c


def sum_list(numbers: list[Union[int, float]]) -> Union[int, float]:
    result = 0
    for number in numbers:
        result += number
    return result

print(add(2, 4))

print(add_with_default(2, 4))

print(sum_list([1,2,3]))


#Eigener Datentype definieren:

Vector = list[float]

def scale(scalar: float, vector: Vector) -> Vector:
    return [num * scalar for num in vector]

print(scale(2.2, [1,2,3,4]))