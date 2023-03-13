import pygame
import button
import csv
import pickle

pygame.init()

# Ventana ------------------------------------------------------------------
# Definimos la ventana principal del editor
screen_width = 1024
screen_height = 768
lower_margin = 150
side_margin = 300
screen = pygame.display.set_mode((screen_width + side_margin, screen_height+lower_margin))

#Definimos colores RGB
LEMON = (231, 245, 195)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

#Definimos variables del juego
ROWS = 16
MAX_COLS = 150
TILE_SIZE = screen_height // ROWS
TILE_TYPES = 44
level = 1
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1
FPS = 60
clock = pygame.time.Clock()
font = pygame.font.SysFont('Minecraft', 25)

#Creamos lista vacia para el mundo
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)
#Creamos un piso
for tile in range(0, MAX_COLS):
    world_data[ROWS - 1][tile] = 0
    
#Funcion para texto en pantalla
def draw_text(text, font, text_col, x, y):
    img =  font.render(text, True, text_col)
    screen.blit(img, (x, y))

# , Definimos nombre a la ventana
pygame.display.set_caption('Py-man: Ryo\'s Oddysey - Part I (Editor de Niveles)')

# Cambiamos el icono del juego
icon = pygame.image.load('Assets/elementos/icon.png')
pygame.display.set_icon(icon)


#Detalles del level editor ---------------------------------------------
#Carga de imagenes
sky_img = pygame.image.load('Assets/escenarios/mounts/m5/2.png').convert_alpha()
pine2_img = pygame.image.load('Assets/escenarios/mounts/m5/4.png').convert_alpha()
clouds1_img = pygame.image.load('Assets/escenarios/mounts/m5/3.png').convert_alpha()
mountain1_img = pygame.image.load('Assets/escenarios/mounts/m5/5.png').convert_alpha()

#Carga de imagenes en lista
img_list = []
for i in range (TILE_TYPES):
    img = pygame.image.load(f'Assets/editor/{i}.png')
    img =  pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

#Cargar botones
save_img = pygame.image.load('Assets/elementos/guardar.png').convert_alpha()
load_img = pygame.image.load('Assets/elementos/cargar.png').convert_alpha()

#-----------------------------------------------------------------------
#Funciones para dibujas elementos---------------------------------------
def draw_bg():
    screen.fill(LEMON)
    width = sky_img.get_width()
    
    #Bucle para scrolling continuo
    for i in range(6):    
        screen.blit(sky_img, ((i *width) - scroll * 0.5, 0))
        screen.blit(clouds1_img, ((i *width) - scroll *0.6, screen_height - clouds1_img.get_height() - 150))
        screen.blit(pine2_img, ((i *width) - scroll * 0.7, screen_height - pine2_img.get_height() - 25))
        screen.blit(mountain1_img, ((i *width) - scroll * 0.8, screen_height - mountain1_img.get_height()))

#Definimos funcion para imprimir el grid posicional
def draw_grid():
    #Lineas verticales
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, screen_height))
    #Lineas horizontales
    for f in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, f * TILE_SIZE), (screen_width, f * TILE_SIZE))
        
#Funcion para dibujar tiles en el mundo
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

#Creacion de botones
save_button = button.Button(screen_width // 2, screen_height + lower_margin - 118, save_img, 1)
load_button = button.Button(screen_width // 2 + 200, screen_height + lower_margin - 122, load_img, 0.9)
        
#Creacion de botones
button_list = []
button_col = 0
button_row = 0

for i in range(len(img_list)):
    tile_button = button.Button(screen_width + (70 * button_col) + 20, 70 * button_row + 25, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    
    if button_col == 4:
        button_row += 1
        button_col = 0

#Bucle para funcionamineto
run = True

while run:
    
    clock.tick(FPS)
    #Llamada de funciones de dibujo
    draw_bg()
    draw_grid()
    draw_world()
    draw_text(f'Level: {level}', font, BLACK, 10, screen_height + lower_margin - 90)
    draw_text('Presiona tecla ARRIBA o ABAJO para cambiar nivel', font, BLACK, 10, screen_height + lower_margin - 60)
    
    #Carga y guardado de datos del mapa
    if save_button.draw(screen):
        #Guarda datos del nivel en un archivo cvs para leerlo en el juego principal
        with open(f'level_{level}_data.csv', 'w', newline ='') as csvfile:
           writer = csv.writer(csvfile, delimiter = ',')       #Delimitador separa los valores del archivo
           for row in world_data:
               writer.writerow(row)
            
    if load_button.draw(screen):
        #Cargar niveles en csv
        #Reinicia el scroll del nivel al inicio
        with open(f'level_{level}_data.csv', newline ='') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')       #Delimitador separa los valores del archivo
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
    
    #Dibujar panel de tiles
    pygame.draw.rect(screen, LEMON, (screen_width, 0, side_margin, screen_height))
    
    
    #Selecciona un tyle
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count
            
    #Resalta el tile seleccionado
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)
    
    #Map scrolling
    if scroll_left == True and scroll > 0:
        scroll -= 5 * scroll_speed  
    if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - screen_width:
        scroll += 5 * scroll_speed  
        
    #Define el arrastre te los tiles en el grid del mundo
    #Obtener posicion del mouse
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) //TILE_SIZE
    y = pos[1] // TILE_SIZE
    
    if pos[0] < screen_width and pos[1] < screen_height:
        #Atualiza el valor del tile
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile #Agregamos el tile seleccionado
                
        if pygame.mouse.get_pressed()[2] == 1:
             world_data[y][x] = -1  #Al dar click derecho, eliminamos el tile del cuadro de grid
                
    #Eventos de cierre del programa
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run =  False
            
        #Teclas presionadas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True 
            if event.key == pygame.K_RSHIFT:
                 scroll_speed = 5  
                     
        #Teclas levantadas
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                 scroll_speed = 1   
        
    pygame.display.update()          
pygame.quit()