/*
 * robot.l - Analizador léxico del lenguaje de robot/dron
 * Autor: Jaime Trujillo Ruiz
 */
%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "robot.tab.h"

extern int errores_lexicos;
%}

%option noyywrap yylineno

%%

"#".*                                   { /* comentario: se ignora hasta el fin de línea */ }
[ \t\r\n]+                              { /* espacios en blanco */ }

"avanzar"                               { return AVANZAR; }
"retroceder"                            { return RETROCEDER; }
"girar"                                 { return GIRAR; }
"izquierda"                             { yylval.dir = -1; return DIRECCION; }
"derecha"                               { yylval.dir = 1;  return DIRECCION; }
"subir"                                 { return SUBIR; }
"bajar"                                 { return BAJAR; }
"repetir"                               { return REPETIR; }
"mostrar"                               { return MOSTRAR; }

[0-9]+("."[0-9]+)?                      { yylval.num = strtod(yytext, NULL); return NUM; }
[a-zA-Z_][a-zA-Z0-9_]*                  { yylval.id = strdup(yytext); return ID; }

"="|"+"|"-"|"*"|"/"|"("|")"|";"|"{"|"}" { return yytext[0]; }

.                                       {
    fprintf(stderr, "Error léxico en línea %d: carácter no válido '%s'\n", yylineno, yytext);
    errores_lexicos++;
}

%%
