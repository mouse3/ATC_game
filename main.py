import pygame
import sys
import random
import time
import math
from pygame.locals import *

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Torre de Control Aérea - Versión Mejorada")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
DARK_GREEN = (0, 100, 0)

# Fuentes
font = pygame.font.SysFont('Arial', 18)
big_font = pygame.font.SysFont('Arial', 30)
small_font = pygame.font.SysFont('Arial', 14)

class Aeropuerto:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = 0
        self.radio = 300  # Radio de control del aeropuerto
        self.pistas_aterrizaje = [1, 2, 3, 4, 5]  # Más pistas de aterrizaje
        self.pistas_despegue = [6, 7, 8]  # Más pistas de despegue
        self.pistas_taxi = ["A", "B", "C", "D", "E"]  # Más pistas de taxi
        self.puertas_embarque = ["G1", "G2", "G3", "G4", "G5"]  # Puertas de embarque
        self.frecuencias = ["121.50", "118.10", "119.70", "120.50", "122.80"]
        self.aviones_en_radio = []
        self.aviones_en_espera = []
        self.mensajes = []
        self.reloj = time.time()
        self.zona_vuelo = self.crear_zona_vuelo()
        self.max_aviones = 10  # Control de densidad de tráfico
        self.tasa_creacion_aviones = 3  # Segundos entre creación de aviones
        
    def crear_zona_vuelo(self):
        # Crear una zona de vuelo irregular
        zona = []
        for i in range(0, 360, 30):
            angulo = math.radians(i)
            variacion = random.randint(50, 150)
            x = self.x + (self.radio + variacion) * math.cos(angulo)
            y = self.y + (self.radio + variacion) * math.sin(angulo)
            zona.append((x, y))
        return zona
        
    def dibujar(self):
        # Dibujar aeropuerto
        pygame.draw.circle(screen, GRAY, (self.x, self.y), 20)
        
        # Dibujar zona de control
        pygame.draw.circle(screen, GRAY, (self.x, self.y), self.radio, 1)
        
        # Dibujar zona de vuelo irregular
        pygame.draw.polygon(screen, (220, 220, 255), self.zona_vuelo, 1)
        
        # Dibujar pistas de aterrizaje (5 pistas)
        pygame.draw.rect(screen, GRAY, (self.x - 200, self.y - 15, 400, 30))  # Pista principal 1 (horizontal)
        pygame.draw.rect(screen, GRAY, (self.x - 15, self.y - 200, 30, 400))  # Pista principal 2 (vertical)
        
        # Pistas diagonales
        pygame.draw.line(screen, GRAY, (self.x - 150, self.y - 150), (self.x + 150, self.y + 150), 30)  # Pista 3
        pygame.draw.line(screen, GRAY, (self.x + 150, self.y - 150), (self.x - 150, self.y + 150), 30)  # Pista 4
        
        # Pista curva (simplificada)
        puntos_pista_5 = []
        for i in range(0, 180, 10):
            angulo = math.radians(i)
            x = self.x + 200 * math.cos(angulo)
            y = self.y - 100 + 100 * math.sin(angulo)
            puntos_pista_5.append((x, y))
        pygame.draw.lines(screen, GRAY, False, puntos_pista_5, 30)
        
        # Dibujar terminales y puertas de embarque
        pygame.draw.rect(screen, (70, 70, 70), (self.x - 120, self.y - 60, 240, 120))  # Terminal principal
        pygame.draw.rect(screen, (50, 50, 50), (self.x + 100, self.y - 40, 80, 80))    # Terminal secundaria
        
        # Dibujar áreas de taxi
        pygame.draw.rect(screen, DARK_GREEN, (self.x - 50, self.y + 40, 100, 60))      # Área de taxi 1
        pygame.draw.rect(screen, DARK_GREEN, (self.x - 120, self.y - 120, 60, 60))     # Área de taxi 2
        
        # Dibujar mensajes
        for i, mensaje in enumerate(self.mensajes[-5:]):  # Mostrar solo los últimos 5 mensajes
            texto = font.render(mensaje, True, BLACK)
            screen.blit(texto, (10, 10 + i * 25))
    
    def verificar_avion_en_radio(self, avion):
        distancia = ((self.x - avion.x) ** 2 + (self.y - avion.y) ** 2) ** 0.5
        if distancia <= self.radio and avion not in self.aviones_en_radio:
            self.aviones_en_radio.append(avion)
            avion.frecuencia = random.choice(self.frecuencias)
            self.mensajes.append(f"Avión {avion.id} entró en zona de radio. Frecuencia: {avion.frecuencia}")
            return True
        elif distancia > self.radio and avion in self.aviones_en_radio:
            self.aviones_en_radio.remove(avion)
            if avion in self.aviones_en_espera:
                self.aviones_en_espera.remove(avion)
            self.mensajes.append(f"Avión {avion.id} salió de zona de radio")
        return False
    
    def asignar_pista(self, avion, tipo_pista, numero_pista=None):
        if tipo_pista == "aterrizaje":
            if self.pistas_aterrizaje:
                pista = self.pistas_aterrizaje.pop(0)
                avion.asignar_pista(tipo_pista, pista)
                self.mensajes.append(f"Avion {avion.id}: Pista de aterrizaje {pista} asignada")
                if avion in self.aviones_en_espera:
                    self.aviones_en_espera.remove(avion)
                return True
        elif tipo_pista == "despegue":
            if self.pistas_despegue:
                pista = self.pistas_despegue.pop(0)
                avion.asignar_pista(tipo_pista, pista)
                self.mensajes.append(f"Avion {avion.id}: Pista de despegue {pista} asignada")
                return True
        elif tipo_pista == "taxi":
            if self.pistas_taxi:
                pista = self.pistas_taxi.pop(0)
                avion.asignar_pista(tipo_pista, pista)
                self.mensajes.append(f"Avion {avion.id}: Pista de taxi {pista} asignada")
                return True
        elif tipo_pista == "puerta":
            if self.puertas_embarque:
                puerta = self.puertas_embarque.pop(0)
                avion.asignar_pista(tipo_pista, puerta)
                self.mensajes.append(f"Avion {avion.id}: Puerta de embarque {puerta} asignada")
                return True
        return False
    
    def poner_en_espera(self, avion):
        if avion not in self.aviones_en_espera:
            self.aviones_en_espera.append(avion)
            avion.poner_en_espera(self.x, self.y)
            self.mensajes.append(f"Avión {avion.id} puesto en espera (stand-by)")
            return True
        return False
    
    def abandonar_area(self, avion):
        if avion in self.aviones_en_radio:
            self.aviones_en_radio.remove(avion)
        if avion in self.aviones_en_espera:
            self.aviones_en_espera.remove(avion)
        avion.abandonar_area()
        self.mensajes.append(f"Avión {avion.id} abandonando área de control")
        return True
    
    def cambiar_frecuencia(self, avion):
        if avion in self.aviones_en_radio:
            nueva_frecuencia = random.choice([f for f in self.frecuencias if f != avion.frecuencia])
            avion.frecuencia = nueva_frecuencia
            self.mensajes.append(f"Avión {avion.id} cambió a frecuencia {nueva_frecuencia}")
            return True
        return False
    
    def actualizar_reloj(self):
        tiempo_transcurrido = int(time.time() - self.reloj)
        horas = tiempo_transcurrido // 3600
        minutos = (tiempo_transcurrido % 3600) // 60
        segundos = tiempo_transcurrido % 60
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
    
    def ajustar_trafico(self):
        # Ajustar la tasa de creación de aviones según la densidad actual
        densidad = len(self.aviones_en_radio) / self.max_aviones
        if densidad < 0.3:
            self.tasa_creacion_aviones = 2  # Más aviones
        elif densidad < 0.6:
            self.tasa_creacion_aviones = 3  # Tasa normal
        else:
            self.tasa_creacion_aviones = 5  # Menos aviones

class Avion:
    def __init__(self, id, x, y, z):
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.velocidad = random.uniform(0.5, 1.5)
        self.velocidad_taxi = 0.3  # Más lento para taxi
        self.direccion = [random.uniform(-1, 1), random.uniform(-1, 1), 0]
        self.radio_colision = 15
        self.pista_aterrizaje = None
        self.pista_despegue = None
        self.pista_taxi = None
        self.puerta_embarque = None
        self.estado = "volando"  # volando, aproximando, aterrizando, rodando, en_puerta, despegando, espera, abandonando
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.angulo_espera = 0
        self.centro_espera_x = 0
        self.centro_espera_y = 0
        self.radio_espera = 120
        self.frecuencia = ""
        self.tiempo_aterrizaje = 0
        self.tiempo_despegue = 0
        self.tiempo_taxi = 0
        self.tiempo_puerta = 0
        self.objetivo_x = 0
        self.objetivo_y = 0
        self.objetivo_z = 0
        self.fase_aterrizaje = 0  # 0: aproximación, 1: descenso, 2: rodaje
        self.aterrizaje_completado = False
    
    def mover(self):
        if self.estado == "volando":
            self.x += self.direccion[0] * self.velocidad
            self.y += self.direccion[1] * self.velocidad
            self.z += self.direccion[2] * self.velocidad
            
            if random.random() < 0.005:
                self.direccion = [random.uniform(-1, 1), random.uniform(-1, 1), 0]
        
        elif self.estado == "aproximando":
            # Mover hacia el punto inicial de la pista
            dx = self.objetivo_x - self.x
            dy = self.objetivo_y - self.y
            dz = self.objetivo_z - self.z
            distancia = (dx**2 + dy**2 + dz**2)**0.5
            
            if distancia < 5:  # Llegó al punto de aproximación
                self.estado = "aterrizando"
                self.fase_aterrizaje = 1
            else:
                # Normalizar dirección
                if distancia > 0:
                    self.x += (dx / distancia) * self.velocidad
                    self.y += (dy / distancia) * self.velocidad
                    self.z += (dz / distancia) * self.velocidad
        
        elif self.estado == "aterrizando":
            if self.fase_aterrizaje == 1:  # Descenso
                self.z -= 0.5
                if self.z <= 10:
                    self.fase_aterrizaje = 2
                    self.velocidad = 0.2  # Reducir velocidad para rodaje
            elif self.fase_aterrizaje == 2:  # Rodaje después de tocar pista
                self.x += (self.objetivo_x - self.x) * 0.02
                self.y += (self.objetivo_y - self.y) * 0.02
                distancia = ((self.objetivo_x - self.x)**2 + (self.objetivo_y - self.y)**2)**0.5
                if distancia < 10:
                    self.estado = "rodando"
                    self.tiempo_aterrizaje = time.time()
                    self.pista_aterrizaje = None  # Liberar pista
        
        elif self.estado == "rodando":
            # Buscar pista de taxi o puerta
            if not self.pista_taxi and not self.puerta_embarque:
                self.objetivo_x = aeropuerto.x + random.randint(-50, 50)
                self.objetivo_y = aeropuerto.y + random.randint(50, 100)
            
            # Mover hacia el objetivo
            dx = self.objetivo_x - self.x
            dy = self.objetivo_y - self.y
            distancia = (dx**2 + dy**2)**0.5
            
            if distancia > 5:
                self.x += (dx / distancia) * self.velocidad_taxi
                self.y += (dy / distancia) * self.velocidad_taxi
            elif not self.puerta_embarque:
                # Solicitar puerta de embarque
                if aeropuerto.asignar_pista(self, "puerta", None):
                    self.objetivo_x = aeropuerto.x + random.randint(-100, -50) if random.random() > 0.5 else aeropuerto.x + random.randint(50, 100)
                    self.objetivo_y = aeropuerto.y + random.randint(-100, 100)
            else:
                # Estacionado en puerta
                if time.time() - self.tiempo_aterrizaje > 10:  # Tiempo en puerta
                    self.estado = "despegando"
                    aeropuerto.puertas_embarque.append(self.puerta_embarque)
                    self.puerta_embarque = None
                    aeropuerto.asignar_pista(self, "despegue", random.choice([6, 7, 8]))
        
        elif self.estado == "despegando":
            if self.z < 100:  # Fase de despegue
                self.z += 0.5
                self.x += self.direccion[0] * self.velocidad * 1.5
                self.y += self.direccion[1] * self.velocidad * 1.5
            else:  # En aire
                self.estado = "volando"
                self.pista_despegue = None
        
        elif self.estado == "espera":
            self.angulo_espera += 0.03
            self.x = self.centro_espera_x + self.radio_espera * math.cos(self.angulo_espera)
            self.y = self.centro_espera_y + self.radio_espera * math.sin(self.angulo_espera)
        
        elif self.estado == "abandonando":
            self.x += self.direccion[0] * self.velocidad * 1.2
            self.y += self.direccion[1] * self.velocidad * 1.2
    
    def dibujar(self):
        color = self.color
        if self.estado == "espera":
            color = ORANGE
        elif self.estado == "abandonando":
            color = RED
        elif self.estado in ["aproximando", "aterrizando"]:
            color = GREEN
        elif self.estado == "despegando":
            color = BLUE
        elif self.estado in ["rodando", "en_puerta"]:
            color = PURPLE
        
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 10)
        
        # Dibujar altitud si está volando
        if self.z > 0:
            alt_text = small_font.render(f"{self.id}: {int(self.z)}m", True, BLACK)
            screen.blit(alt_text, (int(self.x) + 15, int(self.y) - 10))
        
        # Dibujar información de estado
        estado_text = small_font.render(f"{self.estado.upper()}", True, color)
        screen.blit(estado_text, (int(self.x) + 15, int(self.y) + 10))
        
        # Dibujar información de pista/puerta si está asignada
        if self.pista_aterrizaje:
            pista_text = small_font.render(f"Aterr: {self.pista_aterrizaje}", True, GREEN)
            screen.blit(pista_text, (int(self.x) + 15, int(self.y) + 30))
        if self.pista_despegue:
            pista_text = small_font.render(f"Despeg: {self.pista_despegue}", True, BLUE)
            screen.blit(pista_text, (int(self.x) + 15, int(self.y) + 50))
        if self.pista_taxi:
            pista_text = small_font.render(f"Taxi: {self.pista_taxi}", True, PURPLE)
            screen.blit(pista_text, (int(self.x) + 15, int(self.y) + 70))
        if self.puerta_embarque:
            puerta_text = small_font.render(f"Puerta: {self.puerta_embarque}", True, DARK_GREEN)
            screen.blit(puerta_text, (int(self.x) + 15, int(self.y) + 90))
        
        if self.frecuencia:
            freq_text = small_font.render(f"Freq: {self.frecuencia}", True, BLACK)
            screen.blit(freq_text, (int(self.x) + 15, int(self.y) + 110))
    
    def asignar_pista(self, tipo_pista, numero_pista):
        if tipo_pista == "aterrizaje":
            self.pista_aterrizaje = numero_pista
            self.estado = "aproximando"
            
            # Definir punto de aproximación según la pista
            if numero_pista == 1:  # Pista horizontal
                self.objetivo_x = aeropuerto.x - 250
                self.objetivo_y = aeropuerto.y
                self.objetivo_z = 100
            elif numero_pista == 2:  # Pista vertical
                self.objetivo_x = aeropuerto.x
                self.objetivo_y = aeropuerto.y - 250
                self.objetivo_z = 100
            elif numero_pista == 3:  # Pista diagonal 1
                self.objetivo_x = aeropuerto.x - 200
                self.objetivo_y = aeropuerto.y - 200
                self.objetivo_z = 100
            elif numero_pista == 4:  # Pista diagonal 2
                self.objetivo_x = aeropuerto.x + 200
                self.objetivo_y = aeropuerto.y - 200
                self.objetivo_z = 100
            elif numero_pista == 5:  # Pista curva
                self.objetivo_x = aeropuerto.x + 200
                self.objetivo_y = aeropuerto.y - 50
                self.objetivo_z = 100
            
            # Punto final de la pista (donde debe detenerse)
            if numero_pista in [1, 2, 3, 4]:
                self.objetivo_x = aeropuerto.x
                self.objetivo_y = aeropuerto.y
            else:  # Pista curva
                self.objetivo_x = aeropuerto.x + 100
                self.objetivo_y = aeropuerto.y + 50
            
            return True
        
        elif tipo_pista == "despegue":
            self.pista_despegue = numero_pista
            self.estado = "despegando"
            
            # Definir dirección de despegue según la pista
            if numero_pista == 6:  # Usar pista 1 en dirección opuesta
                self.direccion = [1, 0, 0.3]
                self.x = aeropuerto.x - 200
                self.y = aeropuerto.y
            elif numero_pista == 7:  # Usar pista 2 en dirección opuesta
                self.direccion = [0, 1, 0.3]
                self.x = aeropuerto.x
                self.y = aeropuerto.y - 200
            elif numero_pista == 8:  # Usar pista 3 en dirección opuesta
                self.direccion = [0.7, 0.7, 0.3]
                self.x = aeropuerto.x - 150
                self.y = aeropuerto.y - 150
            
            self.z = 0
            return True
        
        elif tipo_pista == "taxi":
            self.pista_taxi = numero_pista
            return True
        
        elif tipo_pista == "puerta":
            self.puerta_embarque = numero_pista
            return True
        
        return False
    
    def poner_en_espera(self, centro_x, centro_y):
        self.estado = "espera"
        self.centro_espera_x = centro_x
        self.centro_espera_y = centro_y
        self.radio_espera = 120 + random.randint(-20, 20)
        self.angulo_espera = math.atan2(self.y - centro_y, self.x - centro_x)
    
    def abandonar_area(self):
        self.estado = "abandonando"
        self.direccion = [self.x - aeropuerto.x, self.y - aeropuerto.y, 0]
        length = (self.direccion[0]**2 + self.direccion[1]**2)**0.5
        if length > 0:
            self.direccion[0] /= length
            self.direccion[1] /= length

def verificar_colision(avion1, avion2):
    # Solo verificar colisión si ambos están volando o aterrizando/despegando
    if (avion1.estado in ["volando", "aproximando", "aterrizando", "despegando"] and 
        avion2.estado in ["volando", "aproximando", "aterrizando", "despegando"]):
        distancia = ((avion1.x - avion2.x) ** 2 + 
                    (avion1.y - avion2.y) ** 2 + 
                    (avion1.z - avion2.z) ** 2) ** 0.5
        return distancia < (avion1.radio_colision + avion2.radio_colision)
    return False

# Crear aeropuerto
aeropuerto = Aeropuerto(WIDTH // 2, HEIGHT // 2)

# Lista de aviones
aviones = []
avion_id = 1

# Tiempo de inicio
start_time = time.time()
juego_activo = True

# Bucle principal
clock = pygame.time.Clock()
input_activo = False
avion_actual = None
tipo_pista_actual = ""
mostrar_opciones = False
mostrar_ayuda = True

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == KEYDOWN and juego_activo:
            if event.key == K_h:
                mostrar_ayuda = not mostrar_ayuda
            
            if not input_activo and event.key == K_c and avion_actual:
                mostrar_opciones = True
            
            if mostrar_opciones:
                if event.key == K_1:
                    mostrar_opciones = False
                    tipo_pista_actual = "aterrizaje"
                    input_activo = True
                elif event.key == K_2:
                    mostrar_opciones = False
                    aeropuerto.poner_en_espera(avion_actual)
                    input_activo = False
                elif event.key == K_3:
                    mostrar_opciones = False
                    aeropuerto.abandonar_area(avion_actual)
                    input_activo = False
                elif event.key == K_4:
                    mostrar_opciones = False
                    aeropuerto.cambiar_frecuencia(avion_actual)
                    input_activo = False
                elif event.key == K_5 and avion_actual.estado == "rodando":
                    mostrar_opciones = False
                    tipo_pista_actual = "taxi"
                    input_activo = True
            
            elif input_activo and tipo_pista_actual == "aterrizaje" and event.key in [K_1, K_2, K_3, K_4, K_5]:
                pista = int(event.unicode)
                if aeropuerto.asignar_pista(avion_actual, tipo_pista_actual, pista):
                    input_activo = False
            elif input_activo and tipo_pista_actual == "despegue" and event.key in [K_6, K_7, K_8]:
                pista = int(event.unicode)
                if aeropuerto.asignar_pista(avion_actual, tipo_pista_actual, pista):
                    input_activo = False
            elif input_activo and tipo_pista_actual == "taxi" and event.key in [K_a, K_b, K_c, K_d, K_e]:
                pista = event.unicode.upper()
                if aeropuerto.asignar_pista(avion_actual, tipo_pista_actual, pista):
                    input_activo = False
    
    # Ajustar tráfico según densidad
    aeropuerto.ajustar_trafico()
    
    # Crear aviones periódicamente
    current_time = time.time()
    if (current_time - start_time > aeropuerto.tasa_creacion_aviones and 
        len(aviones) < aeropuerto.max_aviones and 
        len(aeropuerto.aviones_en_radio) < aeropuerto.max_aviones):
        
        angle = random.uniform(0, 6.28)
        distancia = aeropuerto.radio + 100 + random.randint(0, 200)
        x = aeropuerto.x + distancia * math.cos(angle)
        y = aeropuerto.y + distancia * math.sin(angle)
        
        aviones.append(Avion(avion_id, x, y, random.randint(50, 300)))
        avion_id += 1
        start_time = current_time
    
    # Limpiar pantalla
    screen.fill(WHITE)
    
    # Dibujar aeropuerto
    aeropuerto.dibujar()
    
    # Mover y dibujar aviones
    for avion in aviones[:]:
        avion.mover()
        avion.dibujar()
        
        # Verificar si el avión está en radio del aeropuerto
        if aeropuerto.verificar_avion_en_radio(avion) and avion.estado == "volando" and avion not in aeropuerto.aviones_en_espera:
            avion_actual = avion
        
        # Eliminar aviones que se han ido muy lejos
        if ((avion.x < -200 or avion.x > WIDTH + 200 or 
            avion.y < -200 or avion.y > HEIGHT + 200) and 
            avion.estado == "abandonando"):
            aviones.remove(avion)
    
    # Mostrar reloj y densidad de tráfico
    tiempo = aeropuerto.actualizar_reloj()
    reloj_text = big_font.render(tiempo, True, BLACK)
    screen.blit(reloj_text, (WIDTH - 150, 20))
    
    densidad_text = font.render(f"Aviones: {len(aeropuerto.aviones_en_radio)}/{aeropuerto.max_aviones}", True, BLACK)
    screen.blit(densidad_text, (WIDTH - 150, 50))
    
    # Mostrar opciones de control para el avión actual
    if avion_actual and avion_actual.estado in ["volando", "rodando"] and avion_actual in aeropuerto.aviones_en_radio:
        if not input_activo and not mostrar_opciones:
            screen.blit(font.render(f"Presiona C para controlar avión {avion_actual.id} (Freq: {avion_actual.frecuencia})", True, BLACK), (10, HEIGHT - 70))
        
        if mostrar_opciones:
            pygame.draw.rect(screen, WHITE, (10, HEIGHT - 220, 400, 200))
            pygame.draw.rect(screen, BLACK, (10, HEIGHT - 220, 400, 200), 2)
            
            screen.blit(font.render(f"Opciones para avión {avion_actual.id} (Freq: {avion_actual.frecuencia}):", True, BLACK), (20, HEIGHT - 210))
            
            if avion_actual.estado == "volando":
                screen.blit(font.render("1. Asignar pista de aterrizaje (1-5)", True, GREEN), (20, HEIGHT - 190))
                screen.blit(font.render("2. Poner en espera (stand-by)", True, ORANGE), (20, HEIGHT - 170))
                screen.blit(font.render("3. Abandonar área de control", True, RED), (20, HEIGHT - 150))
                screen.blit(font.render("4. Cambiar frecuencia de radio", True, PURPLE), (20, HEIGHT - 130))
            elif avion_actual.estado == "rodando":
                screen.blit(font.render("5. Asignar pista de taxi (A-E)", True, PURPLE), (20, HEIGHT - 110))
    
    # Mostrar ayuda
    if mostrar_ayuda:
        pygame.draw.rect(screen, (240, 240, 240), (WIDTH - 350, HEIGHT - 250, 340, 240))
        pygame.draw.rect(screen, BLACK, (WIDTH - 350, HEIGHT - 250, 340, 240), 2)
        
        screen.blit(font.render("Controles:", True, BLACK), (WIDTH - 340, HEIGHT - 240))
        screen.blit(font.render("H - Mostrar/ocultar ayuda", True, BLACK), (WIDTH - 340, HEIGHT - 220))
        screen.blit(font.render("C - Controlar avión seleccionado", True, BLACK), (WIDTH - 340, HEIGHT - 200))
        screen.blit(font.render("1-5 - Pistas de aterrizaje", True, GREEN), (WIDTH - 340, HEIGHT - 180))
        screen.blit(font.render("6-8 - Pistas de despegue", True, BLUE), (WIDTH - 340, HEIGHT - 160))
        screen.blit(font.render("A-E - Pistas de taxi", True, PURPLE), (WIDTH - 340, HEIGHT - 140))
        screen.blit(font.render("2 - Poner en espera", True, ORANGE), (WIDTH - 340, HEIGHT - 120))
        screen.blit(font.render("3 - Abandonar área", True, RED), (WIDTH - 340, HEIGHT - 100))
        screen.blit(font.render("4 - Cambiar frecuencia", True, PURPLE), (WIDTH - 340, HEIGHT - 80))
    
    # Verificar colisiones
    for i in range(len(aviones)):
        for j in range(i + 1, len(aviones)):
            if verificar_colision(aviones[i], aviones[j]):
                aeropuerto.mensajes.append(f"COLISIÓN entre avión {aviones[i].id} y avión {aviones[j].id}!")
                juego_activo = False
    
    # Mostrar estado del juego
    if not juego_activo:
        texto = big_font.render("JUEGO TERMINADO - COLISIÓN DETECTADA", True, RED)
        screen.blit(texto, (WIDTH // 2 - 250, HEIGHT // 2 - 30))
    
    pygame.display.flip()
    clock.tick(30)