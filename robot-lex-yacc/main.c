/*
 * main.c - Punto de entrada del intérprete robot/dron
 * Autor: Jaime Trujillo Ruiz
 *
 * Uso: ./robot programa.rob      (o: ./robot < programa.rob)
 *
 * Pasada 1: revisa léxico y sintaxis sin ejecutar nada.
 * Pasada 2: si no hubo errores, ejecuta el programa.
 */
#include <stdio.h>
#include <stdlib.h>

extern FILE *yyin;
extern int yyparse(void);
extern void yyrestart(FILE *f);
extern int yylineno;
extern int errores_sintaxis;
extern void activar_ejecucion(int on);
extern void mostrar_final(void);

int errores_lexicos = 0;

int main(int argc, char **argv) {
    FILE *fuente = stdin;

    if (argc > 1) {
        fuente = fopen(argv[1], "r");
        if (!fuente) {
            perror(argv[1]);
            return 1;
        }
    }

    /* Copia el programa a un archivo temporal para poder leerlo dos veces */
    FILE *copia = tmpfile();
    if (!copia) {
        perror("tmpfile");
        return 1;
    }
    int c;
    while ((c = fgetc(fuente)) != EOF)
        fputc(c, copia);
    if (fuente != stdin)
        fclose(fuente);

    /* Pasada 1: solo sintaxis */
    rewind(copia);
    yyrestart(copia);
    yylineno = 1;
    activar_ejecucion(0);
    yyparse();

    if (errores_lexicos || errores_sintaxis) {
        fprintf(stderr, "Se encontraron %d error(es); el programa no se ejecutó.\n",
                errores_lexicos + errores_sintaxis);
        fclose(copia);
        return 1;
    }

    /* Pasada 2: ejecución */
    rewind(copia);
    yyrestart(copia);
    yylineno = 1;
    activar_ejecucion(1);
    yyparse();
    mostrar_final();

    fclose(copia);
    return 0;
}
