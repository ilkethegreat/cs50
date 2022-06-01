from cs50 import get_int

while True:
    n = get_int("Height: ")
    if n >= 1 and n <= 8:
        break
    else:
        print("Pick a number between 1 and 8, inclusive!")


for i in range(n):
    for space in range(n - i):
        print(" ", end="")
    for j in range(i + 1):
        print("#", end="")
    print()
