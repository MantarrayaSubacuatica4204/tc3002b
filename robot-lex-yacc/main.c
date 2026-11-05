/*
 * main.c - Punto de entrada del intérprete robot/dron
 * Autor: Jaime Trujillo Ruiz
 *
 * Uso: ./robot programa.rob      (o: ./robot < programa.rob)
 */
#include <stdio.h>
#include <stdlib.h>
#include "ast.h"
#include "interp.h"

extern FILE *yyin;
extern int yyparse(void);
extern Node *programa;

int errores_lexicos = 0;
int errores_sintaxis = 0;

int main(int argc, char **argv) {
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
        if (!yyin) {
            perror(argv[1]);
            return 1;
        }
    }

    yyparse();

    if (errores_lexicos || errores_sintaxis) {
        fprintf(stderr, "Se encontraron %d error(es); el programa no se ejecutó.\n",
                errores_lexicos + errores_sintaxis);
        return 1;
    }

    ejecutar(programa);
    return 0;
}
