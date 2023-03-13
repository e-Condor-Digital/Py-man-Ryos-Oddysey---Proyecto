import pygame
import os
import random
import button
import csv

pygame.init()

# Ventana ------------------------------------------------------------------
# Definimos la ventana principal
screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))

# Definimos nombre a la ventana
pygame.display.set_caption('Py-man: Ryo\'s Oddysey - Part I')

# Cambiamos el icono del juego
icon = pygame.image.load('Assets/elementos/icon.png')
pygame.display.set_icon(icon)
# ---------------------------------------------------------------------------

# Variables no mutables ---------------------------------
# Defnimos frame rate
reloj = pygame.time.Clock()
FPS = 60

# Definimos condicoinalidad de funcion del juego
run = True

#Definir variables de accion del personaje
moving_right = False
moving_left = False
attack = False
wizard = False
wizard_thrown = False
ROWS = 16
COLS = 150
TILE_SIZE = screen_height // ROWS
TILE_TYPES = 44
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
credits_screen = False
SCROLL_THRESH = 200
MAX_LEVELS = 3
#Definimos variable para gravedad
gravity = 0.75
# -------------------------------------------------------

# Colores -----------------------------
# Definir color de texto
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
SKYBLUE = (132, 198, 237)
LEMON = (231, 245, 195)
MARCO = (63, 47, 43)
# ------------------------------

# Assests y Fondos ----------------------------------------------------------
# Cargamos el asset del logo del juego
logo = pygame.image.load('Assets/elementos/LOGO.png')

# Carga de assest de botones del juego
start = pygame.image.load('Assets/elementos/start.png').convert_alpha()
credits = pygame.image.load('Assets/elementos/pause.png').convert_alpha()
info = pygame.image.load('Assets/elementos/info.png')

# Cargamos el fondo del juego
#Carga de imagenes
sky_img = pygame.image.load('Assets/escenarios/mounts/m5/2.png').convert_alpha()
pine2_img = pygame.image.load('Assets/escenarios/mounts/m5/4.png').convert_alpha()
clouds1_img = pygame.image.load('Assets/escenarios/mounts/m5/3.png').convert_alpha()
mountain1_img = pygame.image.load('Assets/escenarios/mounts/m5/5.png').convert_alpha()

#Carga de assesta de elemetos del juego
slash = pygame.image.load('Assets/elementos/colect/Icon12.png').convert_alpha()
hechizo_img = pygame.image.load('Assets/elementos/colect/Icon1.png').convert_alpha()

#Elementos recogibles
muni_item = pygame.image.load('Assets/elementos/ficha.png').convert_alpha()
ammo_box = pygame.image.load('Assets/elementos/colect/Icon33.png').convert_alpha()
life_item = pygame.image.load('Assets/elementos/salud.png').convert_alpha()

#Cargamos elementos de inicio
#Cargamos el asset del logo del juego
logo = pygame.image.load('Assets/elementos/LOGO.png')

#Carga de assest de botones del juego
start = pygame.image.load('Assets/elementos/start.png').convert_alpha()
select = pygame.image.load('Assets/elementos/pause.png').convert_alpha()
credits = pygame.image.load('Assets/elementos/credit.png').convert_alpha()
restart = pygame.image.load('Assets/elementos/repeat.png').convert_alpha()

#Carga de background
bg_img = pygame.image.load('Assets/escenarios/ecenario.png').convert()
cred_ban = pygame.image.load('Assets/elementos/credban.png').convert_alpha()
ban = pygame.image.load('Assets/elementos/cred_2.png').convert_alpha()
atras = pygame.image.load('Assets/elementos/return.png').convert_alpha()
#---------------------------------------------------------------------------

#Biblioteca de tiles
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'Assets/editor/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
    
#Diccionario de items
item_boxes = {
    'Health': life_item,
    'Mana': muni_item,
    'Grenade': ammo_box
}

#Definimos la funcion
font = pygame.font.SysFont('Minecraft', 30)
font = pygame.font.SysFont("consolas", 20)

#Funcion para text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
  
#Clase para redimensionar imagen
class Image():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
    def draw(self):
        #Dibuja imagen en pantalla
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
#Definir redimension de imagen
banner_logo = Image(0, 20, cred_ban, 0.65)
cont = Image(500, 80, ban, 1.05)
  
#Funcion para background
def draw_bg():
    screen.fill(LEMON)
    width = sky_img.get_width()  
    for x in range(6):
        screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(clouds1_img, ((x * width) - bg_scroll * 0.6, screen_height - clouds1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - bg_scroll * 0.7, screen_height - pine2_img.get_height() - 25))
        screen.blit(mountain1_img, ((x * width) - bg_scroll * 0.8, screen_height - mountain1_img.get_height()))

#Funcion para reiniciar el nivel
def reset_level():
    shoot_group.empty()
    wizard_group.empty()
    boom_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    #Recargar nivel desde el principio
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)
    
    return data
# ----------------------------------------------------------------------------

# Carga de Personajes y Enemigos ----------------------------
# Carga, escala y posicionamiento del player
class Caballero(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, blade, wizard):
        pygame.sprite.Sprite.__init__(self)
        #Definimos varaiables para cada instancia
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.shoot_cooldown = 0
        self.health = 500
        self.max_health = self.health
        self.blade = blade
        self.start_blade = blade
        self.max_blade = 20
        self.wizard = wizard
        self.start_wizard = wizard
        self.max_wizard = 5
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = [] #Alberga assests de la animacion
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        #Variables especificas para AI enemigos
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20) #(posicion x, posicion y, largo de vista, ancho de vista)
        self.idling = False
        self.idling_counter = 0
        
        #Carga de imagenes secuenciales del player
        animation_types = ['walk', 'run', 'jump', 'dead']
        for animation in animation_types:
            #Reinicia termporalmente la lista de imagenes
            temp_list = []        
            #Define numero de frames de animacion en la carpeta 
            num_of_frames = len(os.listdir(f'Assets/personajes/{self.char_type}/{animation}'))
            #Bucle para albergar los assests de animacion
            for i in range(num_of_frames):
                img = pygame.image.load(f'Assets/personajes/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img) 
            self.animation_list.append(temp_list)
                        
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.width = self.image.get_width()
            self.height = self.image.get_height()
    
    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def move(self, moving_left, moving_right):
        screen_scroll = 0
        #Reiniciar variables de movimiento
        dx = 0
        dy = 0
        
        #Asignamos variables de movimiento
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
            
        #Salto
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
            
        #Aplicamos la gravedad
        self.vel_y += gravity
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y
        
        #Analiza colision con elementos
        for tile in world.obstacle_list:
            #Colision en x direccion
            if tile [1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                #Si la IA colisiona con un muro, se debe girar
                if self.char_type == 'enemies':
                    self.direction *= -1
                    self.move_counter = 0
            #Colision en y direccion
            if tile [1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #Chequear si el suelo es saltable
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #Chequear si hay suelo sobre el ply
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
                    
        #Chequear la colision con el agua
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0
        
        #Chequea la colision con la salida
        level_clear = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_clear = True
        
        
        #Chequear la caida con el fin del mapa
        if self.rect.bottom > screen_height:
            self.health = 0
                    
        #Limitar los bordes del juego
        if self.char_type == 'player':
            if self.rect.left + dx < 0 and self.rect.right + dx > screen_width:
                dx = 0
        
        #Actualizar posicion del movimiento
        self.rect.x += dx
        self.rect.y += dy
        
        #Actualiza el scroll basado en la posocion del jugador
        if self.char_type == 'player':
            if (self.rect.right > screen_width - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - screen_width)\
                or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx
                
        return screen_scroll, level_clear
                
                
    def shoot(self):
        if self.shoot_cooldown == 0 and self.blade > 0:
            self.shoot_cooldown = 20
            shoot = Attack(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            shoot_group.add(shoot)
            self.blade -= 1
    
    #Carga y funcion para la IA de los enemigos
    def ai(self):
        if self.alive and ply.alive:
            if self.idling ==  False and random.randint(1, 200) == 1:
                self.update_action(0) #Accion de caminar (0)
                self.idling = True
                self.idling_counter = 50 
            #Analiza colision de ataque
            if self.vision.colliderect(ply.rect):
                #Detiene animacion y enfrenta al jugador
                self.update_action(0)
                self.shoot()
            else: #Acciones que toma la IA si no ve al jugador en su rango de vision
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1) #Accion de correr (1)
                    self.move_counter += 1
                    #Actualiza el campo de vision de enemigos
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                        #pygame.draw.rect(screen, BLUE, self.vision) .- Presentamos el campo de vision
                        
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
                        
        #Scrolling
        self.rect.x += screen_scroll
            
    def update_animation(self):
        #Timer 
        ANIMATION_COOLDOWN = 100
        #Actualiza la imagen dependiendo del tiempo presente
        self.image = self.animation_list[self.action][self.frame_index]
        #Chequa si el tiempo suficiente ha pasado desde la ultima actualizacion
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #Reinicia la animacion luego de su final
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 4:
                self.frame_index = len(self.animation_list[self.action])-1
            else:
                self.frame_index = 0 
         
    def update_action(self, new_action):
        #Analiza si la nueva acción es diferente de la anterior
        if new_action != self.action:
            self.action = new_action
            #Actualiza las animaciones
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
              
    def check_alive(self):
        if self.health <= 0 :
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3) #Presenta accion de muerte
    
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        #pygame.draw.rect(screen, RED, self.rect, 1)
        
#Creamos una clase para leer el mundo
class World():
    def __init__(self):
        self.obstacle_list = []
        
    def process_data(self, data):
        self.level_length = len(data[0])
        #Iteramos a traves de cada valor en el data del nivel
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 28:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 29 and tile <= 35:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 36: #Jugador
                        #LLamado de personajes    
                        ply = Caballero('player', x * TILE_SIZE, y * TILE_SIZE, 1.3, 8, 20, 5)
                        #Barra de salud
                        health_bar = HealthBar(125, 10, ply.health, ply.health)
                    elif tile == 37: #Enemigos
                        enemy = Caballero('enemies', x * TILE_SIZE, y * TILE_SIZE, 1.5, 3, 20, 0)
                        enemy_group.add(enemy)
                    elif tile == 38: #Ataque item
                        item_box = ItemBox('Mana', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 39: #Granadas / Magia
                        item_box = ItemBox('Grenade', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 40: #Vida item
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile >= 41 and tile <= 42:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile == 43:
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
                    
        return ply, health_bar
    
    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
            
   
# Carga, escala y posicionamiento de decoraciones      
class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)         
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
   
    def update(self):
       self.rect.x += screen_scroll
       
# Carga, escala y posicionamiento de agua     
class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)         
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))     
    
    def update(self):
       self.rect.x += screen_scroll

# Carga, escala y posicionamiento de la salida
class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)         
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    
    def update(self):
       self.rect.x += screen_scroll
            
# Carga, escala y posicionamiento de efectos      
class Attack(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = slash
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        
    def update(self):
        #Movimiento del as de ataque
        self.rect.x += (self.direction * self.speed) + screen_scroll
        #Chequea si el as de ataque ha salido de pantalla
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()
            #Chequea impactos con los tiles
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
                
        #Chequea colisiones con caracteres
        if pygame.sprite.spritecollide(ply, shoot_group, False):
            if ply.alive:
                ply.health -= 50
                self.kill()
        #Chequea colision con caracteres
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, shoot_group, False):
                if enemy.alive:
                    enemy.health -= 50
                    self.kill()
   
   
#Clase para recogibles
class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE//2, y + (TILE_SIZE - self.image.get_height()))
        
    def update(self):
        #Scroll
        self.rect.x += screen_scroll
        #Chequea si el jugador a cogido el item
        if pygame.sprite.collide_rect(self, ply):
            #Chequea que clase de item es
            if self.item_type == 'Health':
                ply.health += 25
                if ply.health > ply.max_health:
                   ply.health = ply.max_health 
            elif self.item_type == 'Grenade':
                ply.wizard += 5
                if ply.wizard > ply.max_wizard:
                   ply.wizard = ply.max_wizard 
            elif self.item_type == 'Mana':
                ply.blade+= 10
                if ply.blade > ply.max_blade:
                   ply.blade = ply.max_blade
            #Borra el item seleccionado
            self.kill()
   
#Clase para barra de salud
class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
        
    def draw(self, health):
        #Actualiza con nueva salud dada por el item
        self.health = health
        #Calcula el ratio de la salud maxima
        ratio = self.health/self.max_health
        pygame.draw.rect(screen, RED, (self.x, self.y, 200, 24))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 200 * ratio, 24))
        pygame.draw.rect(screen, MARCO, pygame.Rect(self.x, self.y, 200, 25),  5, 5)
    
#Clase para hechizos
class Wizard(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -12
        self.speed = 8
        self.image = hechizo_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction
        
    def update(self):
        self.vel_y += gravity
        dx = self.direction * self.speed
        dy = self.vel_y
        
        #Analiza colision con el nivel
        for tile in world.obstacle_list:
             #Chequea si existe colision con las paredes
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
             #Colision en y direccion
            if tile [1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                #Chequear si es lanzado el proyectil
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #Chequear si hay suelo sobre el ply
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
                           
        self.rect.x += dx + screen_scroll
        self.rect.y += dy
        
        #Cuenta regresiva para explosion
        self.timer -= 1
        if self.timer <= 0:
            self.kill()  
            boom = Boom(self.rect.x, self.rect.y, 0.5)
            boom_group.add(boom)
            #Afecta al sprite cercano
            if abs(self.rect.centerx - ply.rect.centerx) < TILE_SIZE * 2 and abs(self.rect.centery - ply.rect.centery) < TILE_SIZE * 2:
                ply.health -=50
                
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 50
                    
            
#Clase para explosiones
class Boom(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        
        #Lista para imagenes para animacion de explosion
        self.images=[]
        
        for i in range(0, 10):
            img = pygame.image.load(f'Assets/elementos/explo/1/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
            self.images.append(img)
            
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
        
    def update(self):
        self.rect.x += screen_scroll
        BOOM_SPPED = 4
        #Actualiza animacion de la explosion
        self.counter += 1
        
        if self.counter >= BOOM_SPPED:
            self.counter = 0
            self.frame_index +=1
            #Elimina la explosion luego de su terminacion
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]
                
#Creamos botones para el juego
start_button = button.Button(screen_width//3, 500, start, 0.8)
credits_button = button.Button(screen_width//3 + 250, 500, credits, 0.8)
restart_button = button.Button(350, 450, restart, 1)
    
#Crear un grupo de sprites
enemy_group = pygame.sprite.Group()
shoot_group = pygame.sprite.Group()
wizard_group = pygame.sprite.Group()
boom_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#Pantalla de inicio del juego -------------------------------
#Definir redimension de imagen
banner_logo = Image(0, 20, cred_ban, 0.65)
cont = Image(500, 80, ban, 1.05)
# ------------------------------------------------------------

#Carga y creacion de niveles-----------------------------------
#Creamos una lista vacia para el mundo
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
    
#Cargar datos del nivel y crear el mundo
with open(f'level_{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter = ",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
ply, health_bar = world.process_data(world_data)
# ------------------------------------------------------------

# Bucle principal del juego ------------------------------
while run:   
    # -------Inicio Zona Draw-----------------------------------------------
    reloj.tick(FPS)

    #Funciones para inicio del juego--------------------------------------
    if start_game ==  False:
    #Menu principal
        #Dibujar menu
        screen.fill(LEMON)
        screen.blit(bg_img, (0 ,0))
        if start_button.draw(screen):
            start_game =  True
        if credits_button.draw(screen):
            credtis_screen =  True
             #Dibujamos el banner del logo
            cont.draw()
            banner_logo.draw()
         #Imprimimos marca de registro
        draw_text("© Grupo 2 - AYED, ESFOT. 2023", font, WHITE, 650, 700)
        screen.blit(logo, (150, 50))
        pass
    else:
    #---------------------------------------------------------------------
        #Background y elementos------------
        draw_bg()
        world.draw()
        screen.blit(info, (0, 0))
        #---------------------------
        #Muestra barra de salud
        health_bar.draw(ply.health)
        
        #Muestra iteraciones de los elementos de armamento
        for x in range(ply.blade):
            screen.blit(slash, (120 + (x * 10), 42))
        for x in range(ply.wizard):
            screen.blit(hechizo_img, (150 + (x * 10), 80))
        
        #Player-------------------------------------------
        ply.update_animation()
        ply.draw()
        
        #Enemmy-------------------------------
        for enemy in enemy_group:
            enemy.ai()
            enemy.update()
            enemy.draw()
    
        #Actualiza y dibuja grupos de elementos
        shoot_group.update()
        wizard_group.update()
        boom_group.update()
        item_box_group.update()
        decoration_group.update()
        water_group.update()
        exit_group.update()
        shoot_group.draw(screen)
        wizard_group.draw(screen)
        boom_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)
            
        if ply.alive:
            #Lanzar ataque
            if attack:
                ply.shoot()
            #Lanzar hechizos
            elif wizard and wizard_thrown == False and ply.wizard > 0:
                wizard = Wizard(ply.rect.centerx + (0.5*ply.rect.size[0]*ply.direction), ply.rect.top, ply.direction)
                wizard_group.add(wizard)
                ply.wizard -= 1
                wizard_thrown = True           
                ply.update_action(4) #Index para atacar (4)
            if ply.in_air:
                ply.update_action(2) #Index para saltar (2)
            #Actualizar acciones del jugador
            elif moving_left or moving_right:
                ply.update_action(1) #Index para correr (1)
            else:
                ply.update_action(0) #Index para caminar (0)
            screen_scroll, level_clear = ply.move(moving_left, moving_right)
            bg_scroll -= screen_scroll 
            #Chequea si el jugador completo el nivel
            if level_clear:
                level += 1
                bg_scroll = 0
                world_data = reset_level()
                if level <= MAX_LEVELS:  
                    #Cargar datos del nivel y crear el mundo
                    with open(f'level_{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter = ",")
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    ply, health_bar = world.process_data(world_data)     
                        
        else: #Muestra una pantalla de reinicio del nivel
            screen_scroll = 0
            if restart_button.draw(screen):
                bg_scroll = 0
                world_data = reset_level()
                #Cargar datos del nivel y crear el mundo
                with open(f'level_{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter = ",")
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                ply, health_bar = world.process_data(world_data)     
        
                
        #-------------------------------------------------
        # -------Fin Zona Draw--------------------------------------------------
    
    #Eventos------------------------------------------
    for event in pygame.event.get():       
        # Evento para cierre de ventana
        if event.type == pygame.QUIT:
            run = False

        #Evento para teclas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_l:
                attack = True
            if event.key == pygame.K_k:
                wizard = True
            if event.key == pygame.K_w and ply.alive: #Salto
                ply.jump = True  
                     
        #Evento para soltar botones del teclado
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a: #Izquierda
                moving_left = False
            if event.key == pygame.K_d: #Derecha
                moving_right = False       
            if event.key == pygame.K_l:
                attack = False
            if event.key == pygame.K_k:
                wizard = False
                wizard_thrown = False
    #----------------------------------------------
                
    pygame.display.update()  # Actualiza la pantalla

pygame.display.update()

pygame.quit()
# ---------------------------------------------------------