"""Help functions """

def call(
    func,
    count,
) -> list:
    """Call function any count of times with init null array of func result"""
    arr = []
    while count >= 1:
        arr.append(func())
        count -= 1
    return arr
