# Intérprete robot/dron con LEX y YACC

**Autor:** Jaime Trujillo Ruiz
**Curso:** Diseño de Compiladores — Tarea 1 (intérprete)

Intérprete de un lenguaje sencillo para programar un robot o un dron. Usa
**flex** (LEX) para el análisis léxico y **bison** (YACC) para el análisis
sintáctico. Se ejecuta dentro de un contenedor Docker.

## Lenguaje

| Instrucción             | Efecto                                                    |
|-------------------------|-----------------------------------------------------------|
| `avanzar N;`            | Avanza N unidades en la dirección actual                  |
| `retroceder N;`         | Retrocede N unidades                                      |
| `girar izquierda;`      | Gira 90° a la izquierda                                   |
| `girar derecha N;`      | Gira N grados a la derecha                                |
| `subir N;`              | Sube N metros (dron)                                      |
| `bajar N;`              | Baja N metros (dron); no puede quedar bajo el suelo       |
| `mostrar;`              | Imprime la posición actual                                |
| `# comentario`          | Se ignora hasta el fin de línea                           |

`N` es un número positivo (por ejemplo `10` o `2.5`).

El robot inicia en `(0, 0)` con rumbo `0` (norte, eje +y). Un rumbo de `90`
apunta al este (eje +x). Al terminar, el intérprete imprime la posición final.

Ejemplo (`ejemplos/demo.rob`), un cuadrado de lado 10:

```
avanzar 10;
girar derecha;
avanzar 10;
girar derecha;
avanzar 10;
girar derecha;
avanzar 10;
girar derecha;
mostrar;
```

## Estructura

```
robot-lex-yacc/
├── robot.l          # Analizador léxico (flex)
├── robot.y          # Gramática; cada instrucción se ejecuta en su acción
├── main.c           # Punto de entrada: revisa sintaxis y luego ejecuta
├── Makefile         # Compilación local
├── Dockerfile       # Imagen Docker con flex, bison y gcc
└── ejemplos/        # Programas de prueba (correctos y con errores)
```

### Cómo funciona

El programa se lee **dos veces**:

1. **Primera pasada:** solo revisa léxico y sintaxis. No mueve nada.
2. **Segunda pasada:** si no hubo errores, ejecuta las instrucciones.

Así, un programa con errores no se ejecuta a medias.

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

Si hay errores léxicos o sintácticos, el programa no se ejecuta.
