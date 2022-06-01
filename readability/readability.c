#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>


int main(void)
{
    string text = get_string("Text: ");

    //Number of letters
    int letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if ((text[i] >= 'a' && text[i] <= 'z') || (text[i] >= 'A' && text[i] <= 'Z'))
        {
            letters++;
        }
    }

    //Number of words
    int words = 1;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == ' ')
        {
            words++;
        }
    }

    //Number of sentences
    int sentences = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }

    // Calculation
    float CLI = (0.0588 * letters / words * 100) - (0.296 * sentences / words * 100) - 15.8;
    int CLIr = round(CLI);

    if (CLIr < 1)
    {
        printf("Before Grade 1\n");
        return 0;
    }
    if (CLIr >= 16)
    {
        printf("Grade 16+\n");
        return 0;
    }
    else
    {
        printf("Grade %i\n", CLIr);
        return 0;
    }
}





