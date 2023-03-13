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

#Carga de assest de botones del juego
carga_img = pygame.image.load('Assets/elementos/carga.png')

#Cambiamos el icono del juego 
icon = pygame.image.load('Assets/elementos/icon.png')
pygame.display.set_icon(icon)

#Variables del juego
game_started = False
game_paused = False        

#Definir fuentes
font = pygame.font.SysFont("DePixel Klein", 32)

#Funcion que define dibujo de texto
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#Definir color de texto
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

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
            
    #-------Inicio Zona Draw-------
    
    screen.blit(carga_img, (0, 275))
     
    #Imprimimos marca de registro
    draw_text("CARGANDO...", font, WHITE, 400, 350)
    
    #-------Fin Zona Draw--------
    pygame.display.update() #Actualiza la pantalla
    reloj.tick(FPS)
    
pygame.quit()
