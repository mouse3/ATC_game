import pygame

DARK_GRAY = (40, 40, 40)

pygame.init()
FONT = pygame.font.SysFont('Arial', 18)
BIG_FONT = pygame.font.SysFont('Arial', 28)

class Aeropuerto:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radio = 300
        self.mensajes = []

    def dibujar(self, screen, font):
        pygame.draw.circle(screen, DARK_GRAY, (self.x, self.y), 20)
        pygame.draw.circle(screen, DARK_GRAY, (self.x, self.y), self.radio, 1)
        pygame.draw.rect(screen, DARK_GRAY, (self.x - 120, self.y - 60, 240, 120), 2)
        screen.blit(font.render("Aeropuerto", True, DARK_GRAY), (self.x - 40, self.y - 10))

