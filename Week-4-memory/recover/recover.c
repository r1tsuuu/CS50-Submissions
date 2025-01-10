#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover filename\n");
        return 1;
    }

    // Open memory card file
    FILE *f = fopen(argv[1], "r");
    if (f == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Buffer to store blocks of 512 bytes
    unsigned char buffer[512];
    FILE *img = NULL; // Pointer to current JPEG file
    char filename[8]; // To store filenames
    int file_count = 0;

    // Read memory card file block by block
    while (fread(buffer, 512, 1, f) == 1)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // Close the current JPEG file, if open
            if (img != NULL)
            {
                fclose(img);
            }

            // Create a new JPEG file
            sprintf(filename, "%03i.jpg", file_count);
            img = fopen(filename, "w");
            if (img == NULL)
            {
                printf("Could not create file %s.\n", filename);
                return 1;
            }
            file_count++;
        }

        // Write the block to the current JPEG file, if open
        if (img != NULL)
        {
            fwrite(buffer, 512, 1, img);
        }
    }

    if (img != NULL)
    {
        fclose(img);
    }
    fclose(f);

    return 0;
}
