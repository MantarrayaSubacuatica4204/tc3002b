# Intérprete robot/dron con LEX y YACC

**Autor:** Jaime Trujillo Ruiz
**Curso:** Diseño de Compiladores — Tarea 1 (intérprete)

Intérprete de un lenguaje sencillo para programar un robot o un dron. Está
construido con **flex** (LEX) para el análisis léxico y **bison** (YACC) para
el análisis sintáctico, y se ejecuta dentro de un contenedor Docker.

## Lenguaje

| Instrucción               | Efecto                                                  |
|---------------------------|---------------------------------------------------------|
| `avanzar expr;`           | Avanza `expr` unidades en la dirección actual           |
| `retroceder expr;`        | Retrocede `expr` unidades                               |
| `girar izquierda;`        | Gira 90° a la izquierda                                 |
| `girar derecha expr;`     | Gira `expr` grados a la derecha                         |
| `subir expr;`             | Sube `expr` metros (dron)                               |
| `bajar expr;`             | Baja `expr` metros (dron); no puede quedar bajo el suelo |
| `repetir expr { ... }`    | Ejecuta el bloque `expr` veces                          |
| `mostrar;`                | Imprime la posición actual                              |
| `variable = expr;`        | Asigna un valor (`+ - * /`, paréntesis y negativos)     |
| `# comentario`            | Se ignora hasta el fin de línea                         |

El robot inicia en `(0, 0)` con rumbo `0` (norte, eje +y). Un rumbo de `90`
apunta al este (eje +x). Al terminar, el intérprete imprime la posición final.

Ejemplo (`ejemplos/demo.rob`):

```
lado = 10;
repetir 4 {
    avanzar lado;
    mostrar;
    girar derecha;
}
```

## Estructura

```
robot-lex-yacc/
├── robot.l          # Analizador léxico (flex)
├── robot.y          # Gramática y precedencias (bison)
├── ast.h / ast.c    # Árbol de sintaxis abstracta
├── interp.h / .c    # Intérprete: recorre el AST y mueve el robot/dron
├── main.c           # Punto de entrada
├── Makefile         # Compilación local
├── Dockerfile       # Imagen Docker con flex, bison y gcc
└── ejemplos/        # Programas de prueba (correctos y con errores)
```

## Compilar y ejecutar con Docker

```bash
docker build -t robot-lex-yacc:local .
docker run --rm robot-lex-yacc:local
docker run --rm -v "$(pwd)/ejemplos:/pruebas:ro" robot-lex-yacc:local /pruebas/dron.rob
```

## Compilar sin Docker (Linux / MSYS2 UCRT64)

Requiere `gcc`, `flex` y `bison`:

```bash
make
./robot ejemplos/demo.rob
```

## Subir la imagen a Docker Hub

Reemplaza `TU_USUARIO` por tu usuario de Docker Hub:

```bash
docker login
docker tag robot-lex-yacc:local TU_USUARIO/robot-lex-yacc:1.0
docker push TU_USUARIO/robot-lex-yacc:1.0
```

Para que otra persona la ejecute:

```bash
docker run --rm TU_USUARIO/robot-lex-yacc:1.0 /app/ejemplos/dron.rob
```

## Errores

- **Léxico:** carácter no válido, por ejemplo `@`. Se reporta la línea.
- **Sintaxis:** falta de `;`, llaves sin cerrar, etc. Se reporta la línea.
- **Ejecución:** variable no definida, división entre cero, o un dron que
  intenta bajar bajo el suelo. Se detiene la ejecución.

Si hay errores léxicos o sintácticos, el programa no se ejecuta.
