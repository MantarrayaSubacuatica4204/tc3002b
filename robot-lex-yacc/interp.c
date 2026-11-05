/*
 * interp.c - Intérprete: recorre el AST y mueve el robot/dron
 * Autor: Jaime Trujillo Ruiz
 *
 * Estado: posición (x, y), altitud z (dron) y rumbo en grados
 * (0 = norte, +y; 90 = este, +x).
 */
#include <math.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "interp.h"

#define PI 3.14159265358979323846

typedef struct Var {
    char       *nombre;
    double      valor;
    struct Var *sig;
} Var;

static Var   *variables = NULL;
static double x = 0, y = 0, z = 0, rumbo = 0;

static void fatal(const char *fmt, ...) {
    va_list ap;
    va_start(ap, fmt);
    fprintf(stderr, "Error de ejecución: ");
    vfprintf(stderr, fmt, ap);
    fprintf(stderr, "\n");
    va_end(ap);
    exit(1);
}

static double obtener_var(const char *nombre) {
    for (Var *v = variables; v; v = v->sig)
        if (strcmp(v->nombre, nombre) == 0)
            return v->valor;
    fatal("la variable '%s' no está definida", nombre);
    return 0;
}

static void asignar(const char *nombre, double valor) {
    for (Var *v = variables; v; v = v->sig) {
        if (strcmp(v->nombre, nombre) == 0) {
            v->valor = valor;
            return;
        }
    }
    Var *nueva = malloc(sizeof *nueva);
    if (!nueva) fatal("sin memoria");
    nueva->nombre = strdup(nombre);
    nueva->valor = valor;
    nueva->sig = variables;
    variables = nueva;
}

static double evaluar(const Node *n) {
    switch (n->tipo) {
    case N_NUM:
        return n->num;
    case N_VAR:
        return obtener_var(n->nombre);
    case N_NEG:
        return -evaluar(n->a);
    case N_BIN: {
        double izq = evaluar(n->a);
        double der = evaluar(n->b);
        switch (n->op) {
        case '+': return izq + der;
        case '-': return izq - der;
        case '*': return izq * der;
        case '/':
            if (der == 0) fatal("división entre cero");
            return izq / der;
        }
        break;
    }
    default:
        break;
    }
    fatal("expresión no válida");
    return 0;
}

/* Avanza 'distancia' en la dirección actual (negativa = retroceder) */
static void mover(double distancia) {
    double rad = rumbo * PI / 180.0;
    x += distancia * sin(rad);
    y += distancia * cos(rad);
}

/* Evita imprimir "-0.00" cuando el error de redondeo deja un valor casi cero */
static double limpia(double v) {
    return fabs(v) < 1e-9 ? 0.0 : v;
}

static void mostrar_estado(const char *etiqueta) {
    printf("%s x=%.2f y=%.2f z=%.2f rumbo=%.1f grados\n",
           etiqueta, limpia(x), limpia(y), limpia(z), limpia(rumbo));
}

static void ejecutar_lista(const Node *n);

static void ejecutar_nodo(const Node *n) {
    switch (n->tipo) {
    case N_ASIGNAR:
        asignar(n->nombre, evaluar(n->a));
        break;
    case N_AVANZAR:
        mover(evaluar(n->a));
        break;
    case N_RETROCEDER:
        mover(-evaluar(n->a));
        break;
    case N_GIRAR: {
        double angulo = n->a ? evaluar(n->a) : 90.0;
        rumbo = fmod(rumbo + n->dir * angulo, 360.0);
        if (rumbo < 0) rumbo += 360.0;
        break;
    }
    case N_SUBIR:
        z += evaluar(n->a);
        break;
    case N_BAJAR: {
        double nueva_z = z - evaluar(n->a);
        if (nueva_z < 0)
            fatal("el dron no puede bajar debajo del suelo (z=%.2f)", nueva_z);
        z = nueva_z;
        break;
    }
    case N_REPETIR: {
        double veces = evaluar(n->a);
        if (veces < 0)
            fatal("repetir necesita un número no negativo");
        for (long i = 0; i < (long)veces; i++)
            ejecutar_lista(n->b->a);
        break;
    }
    case N_MOSTRAR:
        mostrar_estado("Posición:");
        break;
    default:
        fatal("instrucción no válida");
    }
}

static void ejecutar_lista(const Node *n) {
    for (; n; n = n->sig)
        ejecutar_nodo(n);
}

void ejecutar(const Node *programa) {
    ejecutar_lista(programa);
    mostrar_estado("Posición final:");
}
