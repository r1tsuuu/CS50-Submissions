#include <cs50.h>
#include <stdio.h>

bool checkSum(long n);

int main(void)
{
    long input = get_long("Number: ");
    long orig = input;

    int numDigits = 0;
    while (input > 0)
    {
        input /= 10;
        numDigits++;
    }

    if (checkSum(orig))
    {
        long start = orig;
        while (start >= 100)
        {
            start /= 10;
        }
        int firstDigit = start / 10;
        int secondDigit = start % 10;

        if (numDigits == 15 && firstDigit == 3 && (secondDigit == 4 || secondDigit == 7))
        {
            printf("AMEX\n");
        }
        else if (numDigits == 16 && firstDigit == 5 && (secondDigit >= 1 && secondDigit <= 5))
        {
            printf("MASTERCARD\n");
        }
        else if ((numDigits == 13 || numDigits == 16) && firstDigit == 4)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }

    return 0;
}

bool checkSum(long n)
{
    bool everyOtherNum = true;
    int total = 0;

    while (n > 0)
    {
        if (everyOtherNum)
        {
            total += n % 10;
            everyOtherNum = false;
        }
        else
        {
            int otherDigit = (n % 10) * 2;

            if (otherDigit > 9)
            {
                total += (otherDigit % 10);
                total += (otherDigit / 10);
            }
            else
            {
                total += otherDigit;
            }
            everyOtherNum = true;
        }
        n /= 10;
    }

    return (total % 10 == 0);
}
