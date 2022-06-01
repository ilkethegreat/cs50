#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long card;
    do
    {
        card = get_long("Card No: ");
    }
    while (card <= 0);

    int d1, d2, d3, d4, d5, d6, d7, d8;
    d1 = ((card % 100) / 10) * 2;
    d2 = ((card % 10000) / 1000) * 2;
    d3 = ((card % 1000000) / 100000) * 2;
    d4 = ((card % 100000000) / 10000000) * 2;
    d5 = ((card % 10000000000) / 1000000000) * 2;
    d6 = ((card % 1000000000000) / 100000000000) * 2;
    d7 = ((card % 100000000000000) / 10000000000000) * 2;
    d8 = ((card % 10000000000000000) / 1000000000000000) * 2;

    d1 = ((d1 % 100) / 10) + (d1 % 10);
    d2 = ((d2 % 100) / 10) + (d2 % 10);
    d3 = ((d3 % 100) / 10) + (d3 % 10);
    d4 = ((d4 % 100) / 10) + (d4 % 10);
    d5 = ((d5 % 100) / 10) + (d5 % 10);
    d6 = ((d6 % 100) / 10) + (d6 % 10);
    d7 = ((d7 % 100) / 10) + (d7 % 10);
    d8 = ((d8 % 100) / 10) + (d8 % 10);

    int s1 = d1 + d2 + d3 + d4 + d5 + d6 + d7 + d8;
    //Digits that are not going to be multiplied by 2 (starting from the last digit)
    int d9, d10, d11, d12, d13, d14, d15, d16;
    d9 = (card % 10);
    d10 = ((card % 1000) / 100);
    d11 = ((card % 100000) / 10000);
    d12 = ((card % 10000000) / 1000000);
    d13 = ((card % 1000000000) / 100000000);
    d14 = ((card % 100000000000) / 10000000000);
    d15 = ((card % 10000000000000) / 1000000000000);
    d16 = ((card % 1000000000000000) / 100000000000000);

    int s2 = d9 + d10 + d11 + d12 + d13 + d14 + d15 + d16;
    int s3 = s1 + s2;

    if ((s3 % 10) != 0)
    {
        printf("%s\n", "INVALID");
        return 0;
    }
    // VISA, MASTERCARD, AMEX DIFFERENTIATION
    int lengthofthecardnumber = 0;
    long mastercard = card;
    long visa = card;
    long amex = card;

    while (card > 0)
    {
        card = card / 10;
        lengthofthecardnumber++;
    }
    // Identification VISA
    while (visa >= 10)
    {
        visa /= 10;
    }
    if (visa == 4 && (lengthofthecardnumber == 13 || lengthofthecardnumber == 16))
    {
        printf("%s\n", "VISA");
        return 0;
    }
    // Identification AMEX
    while (amex >= 10000000000000)
    {
        amex /= 10000000000000;
    }
    if (lengthofthecardnumber == 15 && (amex == 34 || amex == 37))
    {
        printf("%s\n", "AMEX");
        return 0;
    }
    // Identification MASTERCARD
    while (mastercard >= 100000000000000)
    {
        mastercard /= 100000000000000;
    }
    if (lengthofthecardnumber == 16 && (mastercard == 51 || mastercard == 52 || mastercard == 53 || mastercard == 54
                                        || mastercard == 55))
    {
        printf("%s\n", "MASTERCARD");
        return 0;
    }
    else
    {
        printf("%s\n", "INVALID");
    }
}