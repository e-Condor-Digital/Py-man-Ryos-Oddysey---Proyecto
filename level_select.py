import pygame
from pygame.locals import * 

pygame.init()

#Definimos la ventana principal
screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))
FPS = 30

#Definimos nombre a la ventana
pygame.display.set_caption('Py-man: Ryo\'s Oddysey - Part I')

#Defnimos tiempo de ejecucion
reloj = pygame.time.Clock()

#Definimos condicoinalidad de funcion del juego
run = True

#Cargamos el asset del logo del juego
logo = pygame.image.load('Assets/elementos/LOGO.png')

#Carga de assest de botones del juego
level1 = pygame.image.load('Assets/elementos/leve1.png').convert_alpha()
level2 = pygame.image.load('Assets/elementos/level2.png').convert_alpha()
level3 = pygame.image.load('Assets/elementos/level3.png').convert_alpha()
atras = pygame.image.load('Assets/elementos/return.png').convert_alpha()

#Carga de elementos tipo assets
banner = pygame.image.load('Assets/elementos/banner.png')

#Carga de background
bg_img = pygame.image.load('Assets/escenarios/ecenario.png').convert()
x = 0

#Cambiamos el icono del juego 
icon = pygame.image.load('Assets/elementos/icon.png')
pygame.display.set_icon(icon)

#Clase para poder utilizar fondo animado 

#Clase para botones
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
            
    def draw(self):
        action = False
        #Obtiene posicion del mouse
        pos = pygame.mouse.get_pos()
        #Chequea condiciones de posicionamiento y clickeo del mouse
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                    
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            
        #Dibuja botones en pantalla
        screen.blit(self.image, (self.rect.x, self.rect.y))
            
        return action
        
#Variables del juego
game_started = False
game_paused = False        

#Definir fuentes
font = pygame.font.SysFont("consolas", 20)

#Definir color de texto
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
SKYBLUE = (132, 198, 237)

#Creamos las instancias de los botones
level1_button = Button(200, 400, level1, 0.65)
level2_button = Button(375, 400, level2, 0.65)     
level3_button = Button(550, 400, level3, 0.65)
atras_button = Button(725, 400, atras, 0.65)

#Bucle principal del juego
while run:  
            
    for event in pygame.event.get():  
        #Evento para presion de teclas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_started = True
            
        #Evento para cierre de ventana
        if event.type == pygame.QUIT:
            run = False
                
    #Toma el ancho del fondo y lo divide por una función
    x_relative = x % bg_img.get_rect().width
    screen.blit(bg_img, (x_relative - bg_img.get_rect().width, 0))  #Posicion de la imagen de fondo
        
    if x_relative < screen_width:
        screen.blit(bg_img, (x_relative,0))
        
    x -= 1
        
#-------Inicio Zona Draw-------
        
    screen.blit(banner, (135, 80))

    level1_button.draw()
    level2_button.draw()
    level3_button.draw()
    atras_button.draw()
        
#-------Fin Zona Draw--------
    pygame.display.update() #Actualiza la pantalla
    reloj.tick(FPS)
        
pygame.quit()