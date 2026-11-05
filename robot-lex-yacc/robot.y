/*
 * robot.y - Gramática del lenguaje de robot/dron.
 *
 * Cada instrucción se ejecuta directamente en su acción semántica.
 * Para no ejecutar nada si hay errores, main.c hace dos pasadas:
 *   1) solo revisa la sintaxis (ejecutar_ahora = 0);
 *   2) si no hay errores, ejecuta el programa (ejecutar_ahora = 1).
 *
 * Autor: Jaime Trujillo Ruiz
 */
%{
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int yylex(void);
void yyerror(const char *s);
extern int yylineno;

int errores_sintaxis = 0;

/* Estado del robot/dron: posición, altitud y rumbo en grados (0 = norte) */
static int    ejecutar_ahora = 0;
static double x = 0, y = 0, z = 0, rumbo = 0;

#define PI 3.14159265358979323846

void activar_ejecucion(int on) {
    ejecutar_ahora = on;
}

static double limpia(double v) {
    return fabs(v) < 1e-9 ? 0.0 : v;   /* evita imprimir "-0.00" */
}

static void mostrar(const char *etiqueta) {
    if (!ejecutar_ahora) return;
    printf("%s x=%.2f y=%.2f z=%.2f rumbo=%.1f grados\n",
           etiqueta, limpia(x), limpia(y), limpia(z), limpia(rumbo));
}

static void mover(double distancia) {
    if (!ejecutar_ahora) return;
    double rad = rumbo * PI / 180.0;
    x += distancia * sin(rad);
    y += distancia * cos(rad);
}

static void girar(int dir, double grados) {
    if (!ejecutar_ahora) return;
    rumbo = fmod(rumbo + dir * grados, 360.0);
    if (rumbo < 0) rumbo += 360.0;
}

static void subir(double distancia) {
    if (ejecutar_ahora) z += distancia;
}

static void bajar(double distancia) {
    if (!ejecutar_ahora) return;
    if (z - distancia < 0) {
        fprintf(stderr, "Error de ejecución: el dron no puede bajar debajo del suelo (z=%.2f)\n",
                z - distancia);
        exit(1);
    }
    z -= distancia;
}

void mostrar_final(void) {
    mostrar("Posición final:");
}
%}

%define parse.error verbose

%union {
    double num;
    int    dir;
}

%token <num> NUM
%token <dir> DIRECCION
%token AVANZAR RETROCEDER GIRAR SUBIR BAJAR MOSTRAR

%%

programa
    : %empty
    | programa instruccion
    ;

instruccion
    : AVANZAR NUM ';'              { mover($2); }
    | RETROCEDER NUM ';'           { mover(-$2); }
    | GIRAR DIRECCION ';'          { girar($2, 90); }
    | GIRAR DIRECCION NUM ';'      { girar($2, $3); }
    | SUBIR NUM ';'                { subir($2); }
    | BAJAR NUM ';'                { bajar($2); }
    | MOSTRAR ';'                  { mostrar("Posición:"); }
    | error ';'                    { yyerrok; }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error de sintaxis en línea %d: %s\n", yylineno, s);
    errores_sintaxis++;
}
