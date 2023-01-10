def left_shift(arr, n=1):
    steps = n % len(arr)
    return arr[steps:] + arr[:steps]

a = [[1, 2, 3, 4, 5],
     [6, 7, 8, 9, 10]]

print(a)

a = [left_shift(x) for x in a]

print(a)
