import pygame
from dataclasses import *
from ia import *
import random
import json

class Button:
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft= (x,y)
        self.clicked = False

        
        
    def draw(self,menu):
        global choix_menu
        global message
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                if self.clicked == False:
                    choix_menu = menu
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image,(self.rect.x,self.rect.y))



@dataclass
class Grille:
    pos:list[int] = field(default_factory=list)
    rec_pos:list = field(default_factory=list)
    valeur:int = 1
    def actualiser_grille(self,coordonnée,valeur):
        self.pos[coordonnée] = valeur
    
    def touch_case(self):
        position_souris = pygame.mouse.get_pos()
        for i in range(len(self.rec_pos)):
            if self.rec_pos[i].collidepoint(position_souris):
                if pygame.mouse.get_pressed()[0]:
                    if self.pos[i] == 0:
                        self.pos[i] = self.valeur
                        if self.valeur == 1:
                            self.valeur = 2
                        else:
                            self.valeur = 1
                    
    def colision_grille(self):
        for i in range(len(self.pos)):
            self.rec_pos.append(pygame.Rect(position_dans_grille(i),(50,50)))
            
    def verif_win(self,valeur): #On fait les vérifications de victoires
        #Les lignes
        if self.pos[0]==self.pos[1] and self.pos[0]==self.pos[2] and self.pos[0]==valeur:
            return True
        elif self.pos[3]==self.pos[4] and self.pos[3]==self.pos[5] and self.pos[3]==valeur:
            return True
        elif self.pos[6]==self.pos[7] and self.pos[6]==self.pos[8] and self.pos[6]==valeur:
            return True
        #Les colonnes
        elif self.pos[0]==self.pos[3] and self.pos[0]==self.pos[6] and self.pos[0]==valeur:
            return True
        elif self.pos[1]==self.pos[4] and self.pos[1]==self.pos[7] and self.pos[1]==valeur:
            return True
        elif self.pos[2]==self.pos[5] and self.pos[2]==self.pos[8] and self.pos[2]==valeur:
            return True
        #Les diagonales
        elif self.pos[0]==self.pos[4] and self.pos[0]==self.pos[8] and self.pos[0]==valeur:
            return True
        elif self.pos[2]==self.pos[4] and self.pos[2]==self.pos[6] and self.pos[2]==valeur:
            return True
        else:
            return False
        
    def verif_draw(self):
        compteur = 0
        for i in self.pos:
            if i == 0:
                compteur += 1
        if compteur == 0:
            return True
        else:
            return False

def ajout_partie(user,partie,score):
    with open ("historique.json","r+") as fichier:
        data = json.load(fichier)
        is_user = 0
        for i in data["historique"]:
            if i["user"] == user:
                i["partie"].append(f"Le Joueur {user} a joue une partie en mode {partie} et a {score}")
                is_user = 1
        if is_user == 0:
            data["historique"].append({"user":user,"partie":[f"Le Joueur {user} a joue une partie en mode {partie} et a {score}"]})
        fichier.seek(0)
        json.dump(data,fichier,indent=4)
        
        
pygame.init()

screen = pygame.display.set_mode((600,400))
background = pygame.image.load('backgroun.jpg')
pygame.display.set_caption("Tic Tac Toe")
font = pygame.font.Font('freesansbold.ttf',15)
croixImg = pygame.image.load("croix.png").convert_alpha()
cercleImg = pygame.image.load("cercle.png").convert_alpha()
menu1v1Img = pygame.image.load("Bouton_menu1v1.png").convert_alpha()
menu1v1_button = Button (30,100,menu1v1Img)
menuimpoImg = pygame.image.load("Bouton_menuimpossible.png").convert_alpha()
menuimpossible_button = Button (30, 300,menuimpoImg)
menuezImg = pygame.image.load("Bouton_menuez.png").convert_alpha()
menueasy_button = Button(30,200,menuezImg)
menuImg = pygame.image.load("Bouton_menu.png").convert_alpha()
Menu_button = Button(300,250,menuImg)
input_user = pygame.Rect(200,200,140,32)
def position_dans_grille(index):
    if index == 0:
        return (160,60)
    elif index == 1:
        return (278,60)
    elif index == 2:
        return (400,60)
    elif index == 3:
        return (160,175)
    elif index == 4:
        return (278,175)
    elif index == 5:
        return (400,175)
    elif index == 6:
        return (160,290)
    elif index == 7:
        return (278,290)
    elif index == 8:
        return (400,290)
game_grille = Grille([0,0,0,0,0,0,0,0,0])
game_grille.colision_grille()
choix_menu = -1
run = True
input_active = False
user_text = ""
user_player = ""
ajout_historique = True
while run:
    if choix_menu == -1 :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_user.collidepoint(pygame.mouse.get_pos()):
                    input_active = True
                else:
                    input_active = False
            if input_active == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        input_active = False
                        user_player = user_text
                        choix_menu = 0
                    else: 
                        user_text += event.unicode
        screen.fill((255,255,255))
        screen_text = font.render("Nom d'utilisateur : ",True,(0,0,0))
        screen.blit(screen_text, (180,180))
        pygame.draw.rect(screen,(200,200,250),input_user)
        text_input = font.render(user_text, True, (0, 0, 0))
        screen.blit(text_input, (input_user.x+5, input_user.y+5))
        input_user.w = max(100, text_input.get_width()+10)
        game_grille.pos = [0,0,0,0,0,0,0,0,0]
    elif choix_menu == 0 :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        game_grille.pos = [0,0,0,0,0,0,0,0,0]
        game_grille.valeur = 1
        screen.fill((255,255,255))
        menu1v1_button.draw(1)
        menueasy_button.draw(2)
        menuimpossible_button.draw(3)
        ajout_historique = True
    if choix_menu == 1:
        if game_grille.verif_win(1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            screen.fill((255,255,255))
            text = font.render('La Croix a gagné', True, (255, 0, 0))
            screen.blit(text, (250, 182))
            Menu_button.draw(0)
            if ajout_historique == True:
                ajout_historique = False
                ajout_partie(user_player,"1v1","gagne")
        elif game_grille.verif_win(2):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            screen.fill((255,255,255))
            text = font.render('Le Cercle a gagné', True, (0, 0, 255))
            screen.blit(text, (250, 182))
            Menu_button.draw(0)
            if ajout_historique == True:
                ajout_historique = False
                ajout_partie(user_player,"1v1","perdu")
        elif game_grille.verif_draw():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            screen.fill((255,255,255))
            text = font.render('Egalité', True, (0, 0, 0))
            screen.blit(text, (250, 182))
            Menu_button.draw(0)
            if ajout_historique == True:
                ajout_historique = False
                ajout_partie(user_player,"1v1","fait match nul")
        else:
            screen.fill((35,35,35))
            screen.blit(background, (0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            game_grille.touch_case()
            for i in range(len(game_grille.pos)):
                if game_grille.pos[i] == 1:
                    screen.blit(croixImg,position_dans_grille(i))
                elif game_grille.pos[i] == 2:
                    screen.blit(cercleImg,position_dans_grille(i))
    elif choix_menu == 2:
        if game_grille.verif_win(1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            screen.fill((255,255,255))
            text = font.render('La Joeur a gagné', True, (255, 0, 0))
            screen.blit(text, (250, 182))
            Menu_button.draw(0)
            if ajout_historique == True:
                ajout_historique = False
                ajout_partie(user_player,"IA Simple","gagne")
        elif game_grille.verif_win(2):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            screen.fill((255,255,255))
            text = font.render("L'IA a gagné", True, (0, 0, 255))
            screen.blit(text, (250, 182))
            Menu_button.draw(0)
            if ajout_historique == True:
                ajout_historique = False
                ajout_partie(user_player,"IA Simple","perdu")
        elif game_grille.verif_draw():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            screen.fill((255,255,255))
            text = font.render('Egalité', True, (0, 0, 0))
            screen.blit(text, (250, 182))
            Menu_button.draw(0)
            if ajout_historique == True:
                ajout_historique = False
                ajout_partie(user_player,"IA Simple","fait match nul")
        else:
            screen.fill((35,35,35))
            screen.blit(background, (0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            game_grille.touch_case()
            if game_grille.valeur == 2:
                if game_grille.verif_win(1) == False:
                    if game_grille.verif_draw() == False:
                        ia_simple(game_grille,2)
                        game_grille.valeur = 1
                
            for i in range(len(game_grille.pos)):
                if game_grille.pos[i] == 1:
                    screen.blit(croixImg,position_dans_grille(i))
                elif game_grille.pos[i] == 2:
                    screen.blit(cercleImg,position_dans_grille(i))
    elif choix_menu == 3:
        if game_grille.verif_draw():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            screen.fill((255,255,255))
            text = font.render('Egalité', True, (0, 0, 0))
            screen.blit(text, (250, 182))
            Menu_button.draw(0)
            if ajout_historique == True:
                ajout_historique = False
                ajout_partie(user_player,"IA Dur","fait match nul")
        elif game_grille.verif_win(1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            screen.fill((255,255,255))
            text = font.render("L'Ia a gagné", True, (255, 0, 0))
            screen.blit(text, (250, 182))
            Menu_button.draw(0)
            if ajout_historique == True:
                ajout_historique = False
                ajout_partie(user_player,"IA Dur","perdu")
        elif game_grille.verif_win(2):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            screen.fill((255,255,255))
            text = font.render("Le Joueur a gagné", True, (0, 0, 255))
            screen.blit(text, (250, 182))
            Menu_button.draw(0)
            if ajout_historique == True:
                ajout_historique = False
                ajout_partie(user_player,"IA Dur","gagne")
        else:
            screen.fill((35,35,35))
            screen.blit(background, (0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
           
            if game_grille.valeur == 1:
                if game_grille.verif_draw() == False:
                    ia_hard(game_grille,1)
                    game_grille.valeur=2
            game_grille.touch_case()        
            
            
            for i in range(len(game_grille.pos)):
                if game_grille.pos[i] == 1:
                    screen.blit(croixImg,position_dans_grille(i))
                elif game_grille.pos[i] == 2:
                    screen.blit(cercleImg,position_dans_grille(i))
    pygame.display.update()

pygame.quit()