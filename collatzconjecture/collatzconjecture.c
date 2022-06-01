#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

int collatz(int n);

int main(void)
{
    int n = get_int("integer: ");
    collatz(n);
    return n;
    printf("\n");

    //this part isnt finished
}

int collatz(int n)
{
        if (n == 1)
            return 0;
        else if ((n % 2) == 0)
            return 1 + collatz(n/2);
        else
            return 1 + collatz((3 * n) + 1);
}