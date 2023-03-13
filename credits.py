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

#Cargamos el asset del logo y assests del juego
logo = pygame.image.load('Assets/elementos/LOGO.png')
cred_ban = pygame.image.load('Assets/elementos/credban.png').convert_alpha()
ban = pygame.image.load('Assets/elementos/cred_2.png').convert_alpha()
atras = pygame.image.load('Assets/elementos/return.png').convert_alpha()

#Carga de background
bg_img = pygame.image.load('Assets/escenarios/ecenario.png').convert()
x = 0

#Cambiamos el icono del juego 
icon = pygame.image.load('Assets/elementos/icon.png')
pygame.display.set_icon(icon)

#Cargamos audio del juego
'''audio_1 =  pygame.mixer.Sound('Assets/sonidos/song.ogg')
audio_1.set_volume(0.4)'''

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

#Instancia vboton de retorno
atras_boton = Button(50, 650, atras, 0.40)

#Variables del juego
game_started = False
game_paused = False        

#Bucle principal de prueba
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
    
        #Dibujamos el banner del logo
        cont.draw()
        banner_logo.draw()
        atras_boton.draw()
        #Llamamos la boton de return
        
        #-------Fin Zona Draw--------
        pygame.display.update() #Actualiza la pantalla
        reloj.tick(FPS)
        
pygame.quit()
