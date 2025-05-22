import pygame
import sys
import random
import time
import math
from avion import Avion
from aeropuerto import Aeropuerto
from interfaz import draw_control_panel

# === Constantes ===
WIDTH, HEIGHT = 1600, 900
FPS = 60
MARGEN_SEGURIDAD = 20

WHITE = (255, 255, 255)
LIGHT_GRAY = (230, 230, 230)
DARK_GRAY = (40, 40, 40)

pygame.init()
FONT = pygame.font.SysFont('Arial', 18)
BIG_FONT = pygame.font.SysFont('Arial', 28)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador Aéreo Modularizado")
clock = pygame.time.Clock()

def main():
    aeropuerto = Aeropuerto(600, HEIGHT // 2)
    aviones = [Avion(i + 1, random.randint(100, 1000), random.randint(100, HEIGHT - 100), random.randint(1000, 11000), FONT) for i in range(5)]
    avion_seleccionado = None
    indice_seleccionado = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if mx < 1200:
                    if event.button == 1:
                        for i, avion in enumerate(aviones):
                            if math.hypot(mx - avion.x, my - avion.y) <= 15:
                                avion_seleccionado = avion
                                indice_seleccionado = i
                                for a in aviones:
                                    a.seleccionado = False
                                avion.seleccionado = True
                                break
                    elif event.button == 3 and avion_seleccionado:
                        avion_seleccionado.aplicar_orden(('redirigir', (mx, my)))

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if aviones:
                        if indice_seleccionado is None:
                            indice_seleccionado = 0
                        else:
                            if event.key == pygame.K_DOWN:
                                indice_seleccionado = (indice_seleccionado + 1) % len(aviones)
                            else:
                                indice_seleccionado = (indice_seleccionado - 1) % len(aviones)

                        for i, avion in enumerate(aviones):
                            avion.seleccionado = (i == indice_seleccionado)
                        avion_seleccionado = aviones[indice_seleccionado]

                elif avion_seleccionado:
                    keymap = {
                        pygame.K_e: 'espera',
                        pygame.K_a: 'abandonar',
                        pygame.K_f: 'cambiar_frecuencia',
                        pygame.K_r: 'reanudar',
                        pygame.K_l: 'aterrizar',
                        pygame.K_t: 'taxi',
                        pygame.K_d: 'despegar'
                    }
                    if event.key in keymap:
                        avion_seleccionado.aplicar_orden(keymap[event.key])

        for avion in aviones:
            if time.time() >= avion.proximo_mensaje:
                mensaje = avion.generar_mensaje()
                if mensaje:
                    aeropuerto.mensajes.append(mensaje)
                avion.proximo_mensaje = time.time() + random.randint(30, 70)

        screen.fill(LIGHT_GRAY)
        aeropuerto.dibujar(screen, FONT)
        for avion in aviones:
            avion.mover()
            avion.dibujar(screen)

        draw_control_panel(screen, aviones, FONT, BIG_FONT)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
