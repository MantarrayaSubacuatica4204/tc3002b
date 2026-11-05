/*
 * robot.y - Analizador sintáctico (gramática) del lenguaje de robot/dron
 * Autor: Jaime Trujillo Ruiz
 */
%code requires {
#include "ast.h"
}

%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ast.h"

int yylex(void);
void yyerror(const char *s);
extern int yylineno;
extern int errores_sintaxis;

Node *programa = NULL;   /* raíz del árbol que construye el parser */
%}

%define parse.error verbose

%union {
    double num;
    char  *id;
    int    dir;
    Node  *node;
}

%token <num> NUM
%token <id>  ID
%token <dir> DIRECCION
%token AVANZAR RETROCEDER GIRAR SUBIR BAJAR REPETIR MOSTRAR

%type <node> programa_ stmts stmt bloque expr

/* Precedencia de operadores: de menor a mayor */
%left '+' '-'
%left '*' '/'
%precedence UMENOS

%%

programa_
    : stmts                                  { programa = $1; }
    ;

stmts
    : %empty                                 { $$ = NULL; }
    | stmts stmt                             { $$ = lista_agregar($1, $2); }
    ;

stmt
    : ID '=' expr ';'                        { $$ = nodo_asignar($1, $3); }
    | AVANZAR expr ';'                       { $$ = nodo_unario(N_AVANZAR, $2); }
    | RETROCEDER expr ';'                    { $$ = nodo_unario(N_RETROCEDER, $2); }
    | GIRAR DIRECCION ';'                    { $$ = nodo_girar($2, NULL); }
    | GIRAR DIRECCION expr ';'               { $$ = nodo_girar($2, $3); }
    | SUBIR expr ';'                         { $$ = nodo_unario(N_SUBIR, $2); }
    | BAJAR expr ';'                         { $$ = nodo_unario(N_BAJAR, $2); }
    | REPETIR expr bloque                    { $$ = nodo_repetir($2, $3); }
    | MOSTRAR ';'                            { $$ = nodo_simple(N_MOSTRAR); }
    | error ';'                              { yyerrok; $$ = NULL; }
    ;

bloque
    : '{' stmts '}'                          { $$ = nodo_bloque($2); }
    ;

expr
    : NUM                                    { $$ = nodo_num($1); }
    | ID                                     { $$ = nodo_var($1); }
    | '(' expr ')'                           { $$ = $2; }
    | '-' expr %prec UMENOS                  { $$ = nodo_neg($2); }
    | expr '+' expr                          { $$ = nodo_bin('+', $1, $3); }
    | expr '-' expr                          { $$ = nodo_bin('-', $1, $3); }
    | expr '*' expr                          { $$ = nodo_bin('*', $1, $3); }
    | expr '/' expr                          { $$ = nodo_bin('/', $1, $3); }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error de sintaxis en línea %d: %s\n", yylineno, s);
    errores_sintaxis++;
}
