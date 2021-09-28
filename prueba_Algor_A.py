# Autor: Mayor Moreno Luis Augusto
# Email: lmayormoreno@gmail.com
#  
# Este programa es una prueba propia de A* Pathfinding Algorithm que se tomo de referencia el siguiente video.
# https://www.youtube.com/watch?v=aKYlikFAV4k&t=13s
# 
# Solo se reviso el video una vez y no se colsulto fuentes externas para la realización del mismo.
# Este es la primera version de una serie con el fin de tener un registro del programa y del algoritmo.
# Se espera que se realicen varias versiones posteriores con resultados eficientes y más eficaces.
# En este programa no se llego al resultado esperado pero fue una experiencia entretenida. 
# 
#  Fecha de comienzo:
#    7/21/2021
# 
#  Fecha de finalización:
#    7/27/2021
#
#  Observaciones:
#   * Realizar el programa que sea 100% eficaz
#   * Mejorar la eficiencia del programa
#   * Buscar una mejor manera de graficar el programa
#   * Volver a revisar los conceptos del video de referencia y tenerlos mas en cuenta
#   * Utilizaar las black_list y las white_list
#
#  Motivo de finalización:
#   El programa es muy ineficiente y tengo otro camino por donde dirigirme y cambiaria todo el codigo

import random, math
import pygame as pg

#===============================CLASES===========================
class block:
    # Clase que obtienen los recuadros 
    def __init__(self, i, j, id):
        self.valor = random.randint(0, 100)
        self.i = i 
        self.j = j
        self.color = (255, 255, 255)
        self.vecinos = []
        self.heuristica = 0
        self.pasado = 0
        self.pared = False
        self.es_camino = False
        self.id = id
        self.bloqueado = False

        if random.randint(0, 100) < 30 and not (self.i == bloque_objetivo[0] and self.j == bloque_objetivo[1]):
            self.pared = True
            self.color = (255, 200, 100)

    def dibujar(self, win):
        # Clase que utiliza para dibujar en la pantalla
        pg.draw.rect(win, self.color,(self.i * vector_size + 1, 
                                      self.j * vector_size + 1,
                                      vector_size - 1,
                                      vector_size - 1 
                                    ) )
    def heuristica_calculate(self, destiny):
        #self.heuristica = int(abs(destiny[0] - self.i) + abs(destiny[1] - self.j))  
        self.heuristica = math.sqrt((abs(self.i - destiny[0])) **2 + (abs(self.j - destiny[1])) ** 2)
        if self.es_camino:
            self.heuristica += 0.5

#=============================FUNCIONES=========================
def cargar_vector_2d():
    # Se genera un vector que sirve como grilla para el funcionamiento del programa
    row = width // vector_size
    collumn = height // vector_size
    main_array = [[0 for col in range(collumn)] for row in range(row)]
    contador = 0

    for i in range(len(main_array)):
        for j in range(len(main_array[i])):
            # Dando a una array la cantidad de bloques de la grilla
            main_array[i][j] = block(i, j, contador)
            contador += 1

    for i in range(len(main_array)):
        for j in range(len(main_array[i])):
            # Se agregan los vecinos de los bloques
            if i > 0 and not main_array[i - 1][j].pared:
                main_array[i][j].vecinos.append(main_array[i - 1][j])
            if i < row - 1 and not main_array[i + 1][j].pared:
                main_array[i][j].vecinos.append(main_array[i + 1][j])
            if j > 0 and not main_array[i][j - 1].pared:
                main_array[i][j].vecinos.append(main_array[i][j - 1])
            if j < collumn - 1 and not main_array[i][j + 1].pared:
                main_array[i][j].vecinos.append(main_array[i][j + 1])
    return main_array

# Variables Globales
size = width, height = 1200, 800
vector_size = 25
screen = pg.display.set_mode(size)
pg.display.set_caption("Juego busqueda")
screen.fill((0, 0, 0))
bloqueado = False

#bloque_objetivo = (width // vector_size -1, height // vector_size -1)
bloque_objetivo = [width // vector_size - 1, 0]
bloque_inicial = [0, height //vector_size -1]
bloque_proximo = [0, 0]

def main():
    # Funcion principal que contiene el programa
    grid = cargar_vector_2d()
    CLOCK = pg.time.Clock()
    FPS = 50
    inicio = False
    primera_vuelta = True
    segunda_veulta = True
    white_list = []
    black_list = []
    run = True
    while run:
        # Reloj
        CLOCK.tick(FPS)
        # Receptor de evento
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
                if event.key == pg.K_f:
                    inicio = True
                    print(grid[4][2].vecinos)

                if event.key == pg.K_h:
                    for u in grid[4][2].vecinos:
                        u.color = (0, 255, 0)
                if event.key == pg.K_r:
                    print(grid[bloque_inicial[0]][bloque_inicial[1]].pasado.pasado.i,grid[bloque_inicial[0]][bloque_inicial[1]].pasado.j
                                     ,"/////",grid[bloque_inicial[0]][bloque_inicial[1]].i, grid[bloque_inicial[0]][bloque_inicial[1]].j)
                if event.key == pg.K_p:
                    seguir = input()
                    if seguir == 0:
                        print("Paso....")
                        run = False
        
        # Inicio de la busqueda
        if inicio:
            if len(white_list) == 0 and len(black_list) == 0:
                for i in range (len(grid)):
                    tempo_list = []
                    for j in range(len(grid[i])):
                        tempo_list.append(grid[i][j])
                    white_list.append(tempo_list)

            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    grid[i][j].dibujar(screen)
    
            bloque_actual = grid[bloque_inicial[0]][bloque_inicial[1]]            
            bloque_actual.es_camino = True

            if not bloqueado:
                bloque_actual.color = (0, 255, 0)
                black_list.append(bloque_actual)
                vecino_mayor_heu = 1000
                puede_pasar = True
                for i in bloque_actual.vecinos:
                    if i.pared and i.es_camino:
                        puede_pasar = False

                for i in bloque_actual.vecinos:
                    i.heuristica_calculate(bloque_objetivo)
                    hay_alguno = False
                    if i.heuristica < vecino_mayor_heu and not i.pared and not i.es_camino:
                        vecino_mayor_heu = i.heuristica
                        bloque_inicial[0] = i.i
                        bloque_inicial[1] = i.j
                        hay_alguno = True

                    elif i.heuristica < vecino_mayor_heu and not i.pared and not hay_alguno:
                        vecino_mayor_heu = i.heuristica
                        bloque_inicial[0] = i.i
                        bloque_inicial[1] = i.j
        
                if grid[bloque_inicial[0]][bloque_inicial[1]].es_camino and puede_pasar:# and not grid[bloque_inicial[0]][bloque_inicial[1]].heuristica <= bloque_actual.heuristica:
                    bloque_actual.es_camino = False
                    bloque_actual.pared = True
                    bloque_actual.bloqueado = True
                    bloque_actual.color = (255, 0 ,0)

                grid[bloque_inicial[0]][bloque_inicial[1]].pasado = bloque_actual
                grid[bloque_inicial[0]][bloque_inicial[1]].color = (0, 0, 255)

            else:
                print("Creo que se termino el programa")

            if bloque_actual.i == bloque_objetivo[0] and bloque_actual.j == bloque_objetivo[1]:
                inicio = False

            if primera_vuelta:
                primera_vuelta = False
            if not primera_vuelta and segunda_veulta:
                segunda_veulta = False

        """for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                mouse_i = mouse_pos[0] // vector_size
                mouse_j = mouse_pos[1] // vector_size
                mouse_click = grid[mouse_i][mouse_j]
                print("===============================================")
                print("El valor de camino de la casilla es:", mouse_click.es_camino)
                print(f"El bloque tiene {len(mouse_click.vecinos)}")
                mouse_click.color = (130, 130, 255)"""
                
        pg.display.update()
#==================================================================
if __name__ == "__main__":
    main()