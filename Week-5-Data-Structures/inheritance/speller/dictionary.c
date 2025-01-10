// Implements a dictionary's functionality

#include "dictionary.h"
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Number of buckets in the hash table
#define TABLE_SIZE 50000

// Hash table
node *table[TABLE_SIZE];

// Tracks the number of words loaded into the dictionary
unsigned int word_count = 0;

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hash_value = 0;
    for (int i = 0; word[i] != '\0'; i++)
    {
        hash_value = (hash_value * 31 + tolower(word[i])) %
                     TABLE_SIZE; // Prime multiplier for better distribution
    }
    return hash_value;
}

// Returns true if word is in the dictionary, else false
bool check(const char *word)
{
    unsigned int index = hash(word);
    node *cursor = table[index];

    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0) // Case-insensitive comparison
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        fprintf(stderr, "Error: Could not open dictionary file.\n");
        return false;
    }

    char word[LENGTH + 1];
    while (fscanf(file, "%s", word) != EOF)
    {
        // Allocate memory for a new node
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            fprintf(stderr, "Error: Could not allocate memory for node.\n");
            fclose(file);
            return false;
        }

        // Copy word into the node and initialize the pointer
        strcpy(new_node->word, word);
        new_node->next = NULL;

        // Insert into hash table
        unsigned int index = hash(word);
        new_node->next = table[index];
        table[index] = new_node;

        // Increment the word count
        word_count++;
    }

    fclose(file);
    return true;
}

// Returns the number of words in the dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < TABLE_SIZE; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}
