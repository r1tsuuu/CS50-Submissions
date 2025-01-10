#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

string cipher(string t, int k);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    for (int i = 0; argv[1][i] != 0; i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    int key = atoi(argv[1]);

    if (key < 0)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    string text = get_string("plaintext: ");
    printf("ciphertext: %s\n", cipher(text, key));

    return 0;
}

string cipher(string t, int k)
{
    for (int i = 0; i < strlen(t); i++)
    {
        if (isalpha (t[i]))
        {
            if (islower(t[i]))
            {
                if (t[i] + (k % 26) > 122)
                {
                    t[i] = t[i] + (k % 26) - 26;
                }
                else
                {
                    t[i] = t[i] + (k % 26);
                }
            }
            else
            {
                if (t[i] + (k % 26) > 90)
                {
                    t[i] = t[i] + (k % 26) - 26;
                }
                else
                {
                    t[i] = t[i] + (k % 26);
                }
            }
        }
    }

    return t;
}