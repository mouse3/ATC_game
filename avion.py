import random
import time
import math
import pygame

pygame.init()
FONT = pygame.font.SysFont('Arial', 18)
BIG_FONT = pygame.font.SysFont('Arial', 28)



WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
DARK_GRAY = (40, 40, 40)

PIXEL_TO_KM = 1
KM_TO_PIXEL = 1 / PIXEL_TO_KM
MARGEN_SEGURIDAD = 20


class Avion:
    def __init__(self, id, x, y, z, font):
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.font = font
        self.swak_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))
        self.estado = 'volando'
        self.frecuencia = random.choice(['118.10', '121.50', '120.30'])
        self.color = random.choice([(70, 130, 180), (34, 139, 34), (178, 34, 34), (138, 43, 226)])
        self.velocidad_crucero = random.randint(700, 900)
        self.velocidad = self.velocidad_crucero
        self.direccion = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.seleccionado = False
        self.ultimo_mensaje = time.time()
        self.proximo_mensaje = time.time() + random.randint(30, 70)
        self.objetivo = None

    def mover(self):
        if self.estado in ['abandonando', 'volando']:
            self.velocidad = self.velocidad_crucero

        velocidad_km_por_s = self.velocidad / 3600
        velocidad_px_por_frame = velocidad_km_por_s * KM_TO_PIXEL

        self.x += self.direccion[0] * velocidad_px_por_frame
        self.y += self.direccion[1] * velocidad_px_por_frame

        if self.x < MARGEN_SEGURIDAD:
            self.x = MARGEN_SEGURIDAD
            self.direccion[0] *= -1
        elif self.x > 1200 - MARGEN_SEGURIDAD:
            self.x = 1200 - MARGEN_SEGURIDAD
            self.direccion[0] *= -1

        if self.y < MARGEN_SEGURIDAD:
            self.y = MARGEN_SEGURIDAD
            self.direccion[1] *= -1
        elif self.y > 900 - MARGEN_SEGURIDAD:
            self.y = 900 - MARGEN_SEGURIDAD
            self.direccion[1] *= -1

    def dibujar(self, screen):
        color = ORANGE if self.seleccionado else self.color
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 12)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 12, 2)
        screen.blit(self.font.render(f"ID {self.id}", True, color), (int(self.x) + 15, int(self.y) - 10))
        screen.blit(self.font.render(f"{self.estado.upper()} - {int(self.z)} m", True, DARK_GRAY), (int(self.x) + 15, int(self.y) + 5))
    def aplicar_orden(self, orden):
        if orden == 'espera':
            self.estado = 'espera'
            self.direccion = [0, 0]
        elif orden == 'abandonar':
            self.estado = 'abandonando'
            dx = self.x - 600
            dy = self.y - 450
            norma = math.hypot(dx, dy)
            self.direccion = [dx / norma, dy / norma]
        elif orden == 'cambiar_frecuencia':
            self.frecuencia = random.choice(['118.10', '121.50', '120.30'])
        elif orden == 'reanudar':
            self.estado = 'volando'
        elif orden == 'aterrizar':
            self.estado = 'aterrizando'
        elif orden == 'taxi':
            self.estado = 'rodando'
        elif orden == 'despegar':
            self.estado = 'despegando'
        elif isinstance(orden, tuple) and orden[0] == 'redirigir':
            self.estado = 'redirigido'
            self.direccion = [orden[1][0] - self.x, orden[1][1] - self.y]
            norma = math.hypot(*self.direccion)
            if norma != 0:
                self.direccion[0] /= norma
                self.direccion[1] /= norma

    def generar_mensaje(self):
        mensajes = []
        if self.estado == 'volando':
            mensajes.append(f"Avión {self.id}: Solicito pista de aterrizaje.")
        elif self.estado in ['rodando', 'espera']:
            mensajes.append(f"Avión {self.id}: Listo para despegar.")
            mensajes.append(f"Avión {self.id}: Solicito instrucciones de rodaje.")
        if random.random() < 0.005:
            mensajes.append(f"Avión {self.id}: Reportando emergencia a bordo.")
        return random.choice(mensajes) if mensajes else ""
