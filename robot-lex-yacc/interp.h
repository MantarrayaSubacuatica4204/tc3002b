/*
 * interp.h - Intérprete del lenguaje de robot/dron
 * Autor: Jaime Trujillo Ruiz
 */
#ifndef INTERP_H
#define INTERP_H

#include "ast.h"

/* Ejecuta el programa y muestra la posición final del robot/dron */
void ejecutar(const Node *programa);

#endif
