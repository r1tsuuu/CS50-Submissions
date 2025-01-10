#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

const int POINTS[] = {1, 3, 3, 2,  1, 4, 2, 4, 1, 8, 5, 1, 3,
                      1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
int computeScore(string word);

int main(void)
{
    // get user input
    string player1 = get_string("Player 1: ");
    string player2 = get_string("Player 2: ");

    int score1 = computeScore(player1);
    int score2 = computeScore(player2);

    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }

    return 0;
}

int computeScore(string word)
{
    int total = 0;
    int length = strlen(word);

    for (int j = 0; j < length; j++)
    {
        word[j] = toupper(word[j]);
        if (word[j] >= 65 && word[j] <= 90)
        {
            total += POINTS[word[j] - 65];
        }
    }
    return total;
}