# Dockerfile - Intérprete robot/dron (LEX + YACC)
# Autor: Jaime Trujillo Ruiz

FROM gcc:13

# Herramientas LEX (flex) y YACC (bison) para generar el analizador
RUN apt-get update \
 && apt-get install -y --no-install-recommends flex bison make \
 && rm -rf /var/lib/apt/lists/*

LABEL org.opencontainers.image.title="robot-lex-yacc" \
      org.opencontainers.image.description="Intérprete LEX/YACC para programar robots y drones" \
      org.opencontainers.image.authors="Jaime Trujillo Ruiz"

WORKDIR /app
COPY . .

# Compila el intérprete dentro de la imagen
RUN make

# El contenedor ejecuta el intérprete con el programa indicado
# (por omisión, el ejemplo de demostración)
ENTRYPOINT ["./robot"]
CMD ["ejemplos/demo.rob"]
