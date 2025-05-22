import pygame

WHITE = (255, 255, 255)
DARK_GRAY = (40, 40, 40)
ORANGE = (255, 165, 0)

pygame.init()
FONT = pygame.font.SysFont('Arial', 18)
BIG_FONT = pygame.font.SysFont('Arial', 28)

def draw_control_panel(screen, aviones, font, big_font):
    panel_x = 1200
    panel_width = screen.get_width() - panel_x
    pygame.draw.rect(screen, DARK_GRAY, (panel_x, 0, panel_width, screen.get_height()))

    screen.blit(big_font.render("Controles", True, WHITE), (panel_x + 20, 20))
    # resto del código...

    controles = [
        "Click: Seleccionar avión",
        "Click derecho: Redirigir",
        "E: Espera",
        "A: Abandonar",
        "F: Cambiar frecuencia",
        "R: Reanudar",
        "L: Aterrizar",
        "T: Rodaje",
        "D: Despegar"
    ]
    for i, texto in enumerate(controles):
        screen.blit(FONT.render(texto, True, WHITE), (panel_x + 20, 60 + i * 25))

    screen.blit(BIG_FONT.render("Aviones (SWAK)", True, WHITE), (panel_x + 20, 320))
    for i, avion in enumerate(aviones):
        line = f"ID {avion.id} - {avion.swak_code} - {int(avion.velocidad)} km/h"
        color = ORANGE if avion.seleccionado else WHITE
        screen.blit(FONT.render(line, True, color), (panel_x + 20, 360 + i * 25))
