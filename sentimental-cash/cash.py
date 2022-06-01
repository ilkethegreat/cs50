from cs50 import get_float


def get_cents():
    while True:
        n = get_float("Change: ")
        if n > 0:
            break
    return n


cents = round(int(get_cents() * 100))
quarters = 0
dimes = 0
nickels = 0
pennies = 0

while cents >= 25:
    quarters += 1
    cents -= 25
while cents >= 10:
    dimes += 1
    cents -= 10
while cents >= 5:
    nickels += 1
    cents -= 5
while cents >= 1:
    pennies += 1
    cents -= 1

coinTotal = quarters + dimes + nickels + pennies
print(coinTotal)
