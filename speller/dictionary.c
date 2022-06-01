// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = ((LENGTH * 'z') + 1);

// Hash table
node *table[N];
int wordsTotal = 0;

//
// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int hindex = hash(word);
    node *cursor = table[hindex];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

//
// Hashes word to a number
unsigned int hash(const char *word)
{
    int S = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        S += (toupper(word[i]) - 'A');
    }
    return S;
}

//
// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    //Read one word at a time from the file
    char word[LENGTH + 1]; //(buffer)
    while (fscanf(file, "%s", word) != EOF)
    {
        node *nodeNew = malloc(sizeof(node));
        if (nodeNew == NULL)
        {
            return false;
        }
        //copy the read to the new node
        strcpy(nodeNew->word, word);
        nodeNew->next = NULL;
        //get hashing index
        int hindex = hash(word);
        //Insert the value to the hash table
        if (table[hindex] == NULL)
        {
            table[hindex] = nodeNew;
        }
        else
        {
            nodeNew->next = table[hindex];
            table[hindex] = nodeNew;
        }
        wordsTotal++;
    }
    fclose(file);
    return true;
}

//
// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return wordsTotal;
}

//
// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *head = table[i];
        node *cursor = head;
        node *tmp = head;
        while (cursor != NULL)
        {
            cursor = cursor->next;
            free(tmp);
            tmp = cursor;
        }
    }
    return true;
}
