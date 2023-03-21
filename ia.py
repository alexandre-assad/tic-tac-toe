import random
from dataclasses import *
import pygame

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
                    
            
    def verif(self,valeur): #On fait les vérifications de victoires
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

def ia_simple(grille,valeur):
    try:
        index_alea = random.randint(0,8)
        while grille.pos[index_alea] != 0 : 
            index_alea = random.randint(0,8)
        grille.pos[index_alea] = valeur
    except:
        return False


def minimax(grille,profondeur,joueur):
    if grille.verif_win(1) == True:
        return 1
    elif grille.verif_win(2) == True:
        return -1
    elif grille.verif_draw() == True:
        return 0
    elif profondeur == 0:
        return 0
    
    #Minimax(grille,profondeur+1,joueuropposé)
    if joueur == "joueur":
        bestscore = 100
        for i in range(9):
            if grille.pos[i] == 0:
                grille.pos[i] = 2
                score = minimax(grille,profondeur-1,"ia")
                grille.pos[i] = 0
                score = min(score,bestscore)
                return score
        
    else:
        bestscore = -100
        for i in range(9):
            if grille.pos[i] == 0:
                grille.pos[i] = 1
                score = minimax(grille,profondeur-1,"joueur")
                grille.pos[i] = 0
                score = max(score,bestscore)
                return score
    
    
    
def ia_hard(grille,valeur):
    score :list[int]
    meilleur_score = -10
    meilleur_coup:int
    for i in range(9):
        if grille.pos[i] == 0:
            grille.pos[i] = valeur
            score = minimax(grille,7,"ia")
            grille.pos[i] = 0
            if score > meilleur_score:
                
                meilleur_score = score
                meilleur_coup = i
                print(meilleur_score, meilleur_coup)
    grille.pos[meilleur_coup] = valeur
    

        
        
