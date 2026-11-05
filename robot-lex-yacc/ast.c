/*
 * ast.c - Constructores de nodos del AST
 * Autor: Jaime Trujillo Ruiz
 */
#include <stdio.h>
#include <stdlib.h>
#include "ast.h"

static Node *crear_nodo(TipoNodo tipo) {
    Node *n = calloc(1, sizeof *n);
    if (!n) {
        perror("calloc");
        exit(1);
    }
    n->tipo = tipo;
    return n;
}

Node *nodo_num(double valor) {
    Node *n = crear_nodo(N_NUM);
    n->num = valor;
    return n;
}

Node *nodo_var(char *nombre) {
    Node *n = crear_nodo(N_VAR);
    n->nombre = nombre;
    return n;
}

Node *nodo_bin(char op, Node *izq, Node *der) {
    Node *n = crear_nodo(N_BIN);
    n->op = op;
    n->a = izq;
    n->b = der;
    return n;
}

Node *nodo_neg(Node *expr) {
    Node *n = crear_nodo(N_NEG);
    n->a = expr;
    return n;
}

Node *nodo_asignar(char *nombre, Node *expr) {
    Node *n = crear_nodo(N_ASIGNAR);
    n->nombre = nombre;
    n->a = expr;
    return n;
}

Node *nodo_unario(TipoNodo tipo, Node *expr) {
    Node *n = crear_nodo(tipo);
    n->a = expr;
    return n;
}

/* angulo == NULL significa 90 grados (valor por omisión) */
Node *nodo_girar(int dir, Node *angulo) {
    Node *n = crear_nodo(N_GIRAR);
    n->dir = dir;
    n->a = angulo;
    return n;
}

Node *nodo_repetir(Node *veces, Node *bloque) {
    Node *n = crear_nodo(N_REPETIR);
    n->a = veces;
    n->b = bloque;
    return n;
}

Node *nodo_bloque(Node *lista) {
    Node *n = crear_nodo(N_BLOQUE);
    n->a = lista;
    return n;
}

Node *nodo_simple(TipoNodo tipo) {
    return crear_nodo(tipo);
}

/* Agrega 'nuevo' al final de la lista de instrucciones */
Node *lista_agregar(Node *lista, Node *nuevo) {
    if (!nuevo) return lista;
    if (!lista) return nuevo;
    Node *p = lista;
    while (p->sig) p = p->sig;
    p->sig = nuevo;
    return lista;
}
