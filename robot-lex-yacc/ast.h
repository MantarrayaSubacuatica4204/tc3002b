/*
 * ast.h - Árbol de sintaxis abstracta (AST) del lenguaje de robot/dron
 * Autor: Jaime Trujillo Ruiz
 */
#ifndef AST_H
#define AST_H

typedef enum {
    N_NUM,          /* número literal            */
    N_VAR,          /* variable                  */
    N_BIN,          /* operación binaria         */
    N_NEG,          /* negación unaria           */
    N_ASIGNAR,      /* variable = expresión      */
    N_AVANZAR,      /* avanzar expresión         */
    N_RETROCEDER,   /* retroceder expresión      */
    N_GIRAR,        /* girar izquierda|derecha   */
    N_SUBIR,        /* subir expresión (dron)    */
    N_BAJAR,        /* bajar expresión (dron)    */
    N_REPETIR,      /* repetir expresión bloque  */
    N_MOSTRAR,      /* mostrar posición          */
    N_BLOQUE        /* { lista de instrucciones } */
} TipoNodo;

typedef struct Node {
    TipoNodo     tipo;
    double       num;     /* N_NUM                     */
    char         op;      /* N_BIN: '+', '-', '*', '/' */
    int          dir;     /* N_GIRAR: -1 izquierda, 1 derecha */
    char        *nombre;  /* N_VAR, N_ASIGNAR          */
    struct Node *a;       /* operando / expresión      */
    struct Node *b;       /* segundo operando / bloque */
    struct Node *sig;     /* siguiente instrucción     */
} Node;

Node *nodo_num(double valor);
Node *nodo_var(char *nombre);
Node *nodo_bin(char op, Node *izq, Node *der);
Node *nodo_neg(Node *expr);
Node *nodo_asignar(char *nombre, Node *expr);
Node *nodo_unario(TipoNodo tipo, Node *expr);
Node *nodo_girar(int dir, Node *angulo);
Node *nodo_repetir(Node *veces, Node *bloque);
Node *nodo_bloque(Node *lista);
Node *nodo_simple(TipoNodo tipo);
Node *lista_agregar(Node *lista, Node *nuevo);

#endif
