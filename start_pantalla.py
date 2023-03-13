import pygame
import button
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
start = pygame.image.load('Assets/elementos/start.png').convert_alpha()
pause = pygame.image.load('Assets/elementos/pause.png').convert_alpha()
credits = pygame.image.load('Assets/elementos/credit.png').convert_alpha()

#Carga de background
bg_img = pygame.image.load('Assets/escenarios/ecenario.png').convert()
x = 0

#Cambiamos el icono del juego 
icon = pygame.image.load('Assets/elementos/icon.png')
pygame.display.set_icon(icon)

#Cargamos audio del juego
audio_1 =  pygame.mixer.Sound('Assets/sonidos/song.ogg')
audio_1.set_volume(0.4)

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

#Funcion que define dibujo de texto
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
    
#Creamos las instancias de los botones
start_button = Button(300, 500, start, 0.65)
pause_button = Button(450, 500, pause, 0.65)     
credit_button = Button(600, 500, credits, 0.65)

#Bucle principal del juego
while run:  
    
    audio_1.play()
         
    for event in pygame.event.get():  
        #Evento para presion de teclas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_started = True
        
        #Evento para cierre de ventana
        if event.type == pygame.QUIT:
            run = False
            
    #Toma el ancho del fondo y lo divide por una función
   
    
    #-------Inicio Zona Draw-------
    
    #Dibujamos el logo
    screen.blit(logo, (150, 50))
    
    #Imprimimos marca de registro
    draw_text("© Grupo 2 - AYED, ESFOT. 2023", font, WHITE, 650, 700)
    
    if game_started == True: #Evento que al presionar tecla, pasa al siguiente apartado
        pass
        #Menu en pantalla
    
    if start_button.draw() == True:
        pass

    if pause_button.draw() ==  True:
        pass
        
    if credit_button.draw() == True:
        pass
    
    #-------Fin Zona Draw--------
    pygame.display.update() #Actualiza la pantalla
    reloj.tick(FPS)
    
pygame.quit()
