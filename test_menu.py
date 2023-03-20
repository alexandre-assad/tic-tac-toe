import pygame
from dataclasses import *

class Button:
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft= (x,y)
        self.clicked = False

        
        
    def draw(self):
        global choix_menu
        global message
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                if self.clicked == False:
                    choix_menu = 1
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image,(self.rect.x,self.rect.y))








pygame.init()


screen = pygame.display.set_mode((600,400))
background = pygame.image.load('backgroun.jpg')
pygame.display.set_caption("Jeux de rôle")
font = pygame.font.Font('freesansbold.ttf',25)
croixImg = pygame.image.load("croix.png").convert_alpha()
cercleImg = pygame.image.load("cercle.png").convert_alpha()
menu1v1Img = pygame.image.load("Bouton_menu1v1.png").convert_alpha()
menu1v1_button = Button (100,200,menu1v1Img)
choix_menu = 0
run = True
while run:
    if choix_menu == 0 :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        screen.fill((255,255,255))
        menu1v1_button.draw()
    pygame.display.update()
    
pygame.quit()