/* Dimacs graph format translator to and from a binary, more efficient
   format. Written by Tamas Badics (badics@rutcor.rutgers.edu),
   using the technique of Marcus Peinado. */

/* Marcus Peinado
   Department of Computer Science
   Boston University
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "genbin.h"

/* Prototypes */
static int  get_params(void);
static BOOL get_edge(int i, int j);
static void write_graph_DIMACS_ascii(const char *file);
static void read_graph_DIMACS_bin(const char *file);

/* ====================================================== */

static BOOL get_edge(int i, int j)
{
    int byte, bit;
    unsigned char mask;

    bit  = 7 - (j & 0x00000007);
    byte = j >> 3;

    mask = (unsigned char)masks[bit];
    return ((Bitmap[i][byte] & mask) == mask);
}

/* ============================================= */

static void write_graph_DIMACS_ascii(const char *file)
{
    int i, j;
    FILE *fp;

    fp = fopen(file, "w");
    if (fp == NULL) {
        printf("ERROR: Cannot open outfile\n");
        exit(10);
    }

    fprintf(fp, "%s", Preamble);

    for (i = 0; i < Nr_vert; i++) {
        for (j = 0; j <= i; j++) {
            if (get_edge(i, j)) {
                fprintf(fp, "e %d %d\n", i + 1, j + 1);
            }
        }
    }

    fclose(fp);
}

static void read_graph_DIMACS_bin(const char *file)
{
    int i;
    int length = 0;
    FILE *fp;

    fp = fopen(file, "rb");   /* IMPORTANT: binary read */
    if (fp == NULL) {
        printf("ERROR: Cannot open infile\n");
        exit(10);
    }

    if (fscanf(fp, "%d\n", &length) != 1) {
        printf("ERROR: Corrupted preamble.\n");
        exit(10);
    }

    if (length >= MAX_PREAMBLE) {
        printf("ERROR: Too long preamble.\n");
        exit(10);
    }

    if ((int)fread(Preamble, 1, (size_t)length, fp) != length) {
        printf("ERROR: Corrupted preamble.\n");
        exit(10);
    }
    Preamble[length] = '\0';

    if (!get_params()) {
        printf("ERROR: Corrupted preamble.\n");
        exit(10);
    }

    /* Read bitmap rows */
    for (i = 0; i < Nr_vert; i++) {
        size_t row_bytes = (size_t)((i + 8) / 8);
        if (fread(Bitmap[i], 1, row_bytes, fp) != row_bytes) {
            break;
        }
    }

    fclose(fp);
}

static int get_params(void)
/* Get Nr_vert and Nr_edges from the preamble string,
   containing Dimacs format "p ??? num num" */
{
    char c;
    char tmp[100];
    char *pp = Preamble;
    int stop = 0;

    Nr_vert = 0;
    Nr_edges = 0;

    while (!stop && (c = *pp++) != '\0') {
        switch (c) {
            case 'c':
                while ((c = *pp++) != '\n' && c != '\0') { }
                break;

            case 'p':
                /* after 'p' we parse: type, Nr_vert, Nr_edges */
                if (sscanf(pp, "%99s %d %d", tmp, &Nr_vert, &Nr_edges) == 3) {
                    stop = 1;
                } else {
                    return 0;
                }
                break;

            default:
                break;
        }
    }

    if (Nr_vert == 0 || Nr_edges == 0)
        return 0;
    return 1;
}

/* ============================================= */

int main(int argc, char *argv[])
{
    int i;
    char name[255];

    if (argc > 3 || argc < 2) {
        printf("Usage: %s infile [outfile]\n", argv[0]);
        return 10;
    }

    if (argc == 2) {
        /* default output name: remove ".b" from input */
        strncpy(name, argv[1], sizeof(name) - 1);
        name[sizeof(name) - 1] = '\0';

        i = (int)strlen(name) - 1;

        if (i >= 1 && name[i] == 'b' && name[i - 1] == '.') {
            name[i - 1] = '\0'; /* remove ".b" */
        } else {
            printf("ERROR: Wrong input file name.\n");
            return 10;
        }
    } else {
        strncpy(name, argv[2], sizeof(name) - 1);
        name[sizeof(name) - 1] = '\0';
    }

    read_graph_DIMACS_bin(argv[1]);
    write_graph_DIMACS_ascii(name);

    return 0;
}