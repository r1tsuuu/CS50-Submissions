#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int countWords(string t);
int countSentences(string s);
int countLetters(string j);
int main(void)
{
    string text = get_string("Text: ");
    int words = countWords(text);
    int sentences = countSentences(text);
    int letters = countLetters(text);

    // the average number of letters per 100 words in the text,
    float L = (letters / (float) words) * 100;
    // the average number of sentences per 100 words in the text
    float S = (sentences / (float) words) * 100;

    float index = 0.0588 * L - 0.296 * S - 15.8;
    int gradeLevel = round(index);

    if (gradeLevel < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (gradeLevel >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", gradeLevel);
    }
    return 0;
}

int countLetters(string j)
{
    int letterCount = 0;
    int length = strlen(j);
    for (int i = 0; i < length; i++)
    {
        if (isalpha(j[i]))
        {
            letterCount++;
        }
    }
    return letterCount;
}

int countWords(string t)
{
    int wordCount = 1;
    int length = strlen(t);
    for (int i = 0; i < length; i++)
    {
        if (t[i] == ' ')
        {
            wordCount++;
        }
    }
    return wordCount;
}

int countSentences(string s)
{
    int sentenceCount = 0;
    int length = strlen(s);
    for (int i = 0; i < length; i++)
    {
        if (s[i] == '.' || s[i] == '!' || s[i] == '?')
        {
            sentenceCount++;
        }
    }
    return sentenceCount;
}