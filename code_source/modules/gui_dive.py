# Grégory Coutable 2025
# Partage sous licence Creative Commons :
# https://creativecommons.org/licenses/by-sa/3.0/fr/
#
# Version :
# 1.2 : inclus ordi, mano, profil, heure. fenetre taille fixe
# 1.3 : fenètre redimensionnable
# 2.1 : nouvelle gestion du temps. incompatible avec les versions précédentes
# 2.2 : avec profil fond defilant
# 2.3 : Bouton affiche deco
# 2.4 : Préparation pour l'appli standalone

__autor__ = 'Grégory COUTABLE'
__version__ = '2.4'
__date__ = '19/11/2026'
print(f"Interface utilisateur graphique (GIU) : version : {__version__}, {__name__}")

import pygame
from pygame.locals import *
import time
import sys
from copy import deepcopy
from modules.constantes import *
 
#pour le rendre dispo de n'importe où
import os
pathname = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
    
class GUIdive (object):
    def __init__(self):
        """
        
        
        """
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        #initialisation de pygame
        pygame.init()

        #on définit la fenêtre de base de notre jeuW_BASE, H_BASE
        self.window = pygame.display.set_mode((600, 400), RESIZABLE)
        #un titre sur cette fenêtre
        pygame.display.set_caption("Simulateur de plongée")
        
        self.computer = None
        self.bloc = None
        self.profil = None
        
        self.img_fond = pygame.Surface((W_BASE, H_BASE), pygame.SRCALPHA)
        self.img_fond.fill(COLOR_FOND)
        self.scale = 1
        
        self.bp = [Bouton(WBP, HBP, txt) for txt in LIST_BP_BAS]
        
        
        for i in range(len(self.bp)):
            self.bp[i].setRect(XBP + i * (WBP + DBP), YBP)
        
        # Ajout des boutons spéciaux
        # mode deco : 2bp
        self.bp.append(self.bp[6].copy(BP_DEC_MDE))
        self.bp.append(Bouton(WBP_DECO, HBP, BP_DEC_EN))
        self.bp[-1].setRect((W_DECO - WBP_DECO) // 2, YBP - 300)
        # aide
        self.bp.append(Bouton(WBP_HELP, HBP, BP_HELP, 72))
        self.bp[-1].setRect(X_BP_HELP, Y_BP_HELP)
        
        self.police_speed = pygame.font.Font(os.path.join(pathname, ASSETS, POLICE_SPEED), W_SPEED)
        self.police_heure = pygame.font.Font(os.path.join(pathname, ASSETS, POLICE_HEURE), W_HEURE)

        self.clock = pygame.time.Clock()
        self.init_heure()
        
    def visible_bp(self, lst_i_bp=None):
        if lst_i_bp is None:
            lst_i_bp = list(range(len(self.bp)))
        for i in range(len(self.bp)):
            if i in lst_i_bp:
                self.bp[i].visible()
            else:
                self.bp[i].invisible()
        
    def init_heure(self):
        self.visible_bp([1, 2, 7, 11]) # 'DOWN++', 'FASTER', 'SLOWER'
        self.heure = HEURE_INIT * 3600
        self.defilement_fond = 0

    def set_computer(self, computer):
        self.computer = computer
        
    def set_profil(self, profil):
        self.profil = profil
        
    def set_bloc(self, bloc):
        self.bloc = bloc
        
    def creer_surface(self, speed, pause):
        """Créé la surface d'affichage de taille W_BASE, H_BASE
        """
        surface = pygame.Surface((W_BASE, H_BASE))
        surface.blit(self.img_fond, (0, 0))
        
        surface.blit(*self._get_surface_heure())
        
        if self.computer is not None:
            surface.blit(self.computer.get_image(speed, pause), (0, 20))
            
        if not pause:
            self.defilement_fond += speed / 150
            
        if self.profil is not None:
            surface.blit(self.profil.get_image(d_x=self.defilement_fond,
                                               anim=not pause or self.heure == HEURE_INIT * 3600,
                                               prof=self.computer.prof),
                                               (X_PROFIL, Y_PROFIL))
            
        if self.bloc is not None and self.computer.mode != 3:
            image_mano = self.bloc.get_image_mano()
            mano_rect = image_mano.get_rect()
            mano_rect.bottom = Y_PROFIL + H_PROFIL - MARGE_MANO
            mano_rect.right = X_PROFIL + W_PROFIL - MARGE_MANO
            surface.blit(image_mano, mano_rect)
        
        for bp in self.bp:
            surface.blit(bp.image, bp.rect)
            
        txt = self.police_speed.render('SPEED X' + str(speed), True, COLOR_SPEED) # pygame.Color('#FFFFFF'))
        txt_rect = txt.get_rect()
        txt_rect.left = X_SPEED
        txt_rect.bottom = Y_SPEED
        surface.blit(txt, txt_rect)
        
        return surface

    def refresh(self, speed, pause):
        """
        Cette méthode rafraichie l'affichage de la fenètre.
        
        paramètres
        ----------
        speed : int
            vitesse de défilement de la plongée, > 1, pour *1
        pause : bool
            bloque l'affichage de l'ordi quand la plongée est en pause. Si True, affichage figé
            important pour le décompte du palier de sécu.
        """
        
        if not pause:
            self.heure += INTERVAL_MESURE * speed
            if self.heure >= 86400:
                self.heure = 0
        # image du GUI en taille de base
        surface = self.creer_surface(speed, pause)
        # adaptation a la taille de la fenetre
        surf_ratio = W_BASE / H_BASE
        win_w, win_h = self.window.get_size()
        win_ratio = win_w / win_h
        win_center = win_w // 2, win_h // 2
        
        if win_ratio < surf_ratio:
            im_w = win_w
            im_h = round(im_w / surf_ratio)
        else:
            im_h = win_h
            im_w = round(im_h * surf_ratio)
            
        self.scale = (im_w / W_BASE + im_h / H_BASE) / 2
        
        # on prèvoit une marge de recadrage de 2 px tout autour
        # car la remise a l'echelle produit souvent une ligne blanche.
        # on recadre cette image ensuite
        image_marge = pygame.transform.smoothscale(surface, (im_w + 4, im_h + 4))
        image = pygame.Surface((im_w, im_h))
        image.blit(image_marge, (-2, -2))
        image_rect = image.get_rect(center=win_center)

        self.window.fill((30, 30, 30))
        self.window.blit(image, image_rect)

        pygame.display.update()

    def _get_surface_heure(self):
        heure = int(self.heure)
        h = heure // 3600
        m = (heure - h * 3600) // 60
        s = heure % 60
        ajoute_0 = lambda x: '0' if x < 10 else ''
        text = f'{ajoute_0(h)}{h}:{ajoute_0(m)}{m}:{ajoute_0(s)}{s}'
        txt = self.police_heure.render(text, True, COLOR_HEURE)
        txt_rect = txt.get_rect()
        txt_rect.left = X_HEURE
        txt_rect.top = Y_HEURE
        return (txt, txt_rect)
    
    def _xy_convert(self, pos_i):
        # reference au centre de l'écran
        win_w, win_h = self.window.get_size()
        xi_c, yi_c = pos_i[0] - win_w // 2, pos_i[1] - win_h // 2
        # remise a l'echelle
        xs_c, ys_c = xi_c // self.scale, yi_c // self.scale
        # replacer au centre de l'image de base
        return xs_c + W_BASE // 2, ys_c + H_BASE // 2        

    def waitClick(self, nDiziemeSeconde=None):
        """
        Cette méthode attend l'action d'un joueur. Elle gère plusieurs types d'actions :
            - demande fermeture de la fenètre : fermeture propre de la fenètre pygame et fin du programme python.
            - Quelques autres touches sont également gérées et retourne la lettre saisie.
        Si le paramètre optionel nDiziemeSeconde est None (valeur par défaut), on ne peut sortir de cette méthode que par
        l'une de ces actions. Si le paramètre nDiziemeSeconde est fixé à une valeur non nulle, la boucle est interrompue après ce
        temps.

        """
            
        while nDiziemeSeconde is None or nDiziemeSeconde > 0:
            if nDiziemeSeconde is not None:
                nDiziemeSeconde -= 1
                
            self.clock.tick(10)#attend 1 dizieme de seconde

            for event in pygame.event.get():    #Attente des événements
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 or event.button == 3:   #Si clic gauche ou droit
                        pos_sur_base = self._xy_convert(event.pos)
                        for i in range(len(self.bp)):
                            if self.bp[i].isCollide(pos_sur_base):
                                return F'BP{i}'                            
                
                if event.type == KEYDOWN:
                    touches = {K_RIGHT : '_R', K_LEFT : '_L', K_UP : '_U', K_DOWN : '_D', K_RETURN : '_E', K_BACKSPACE : '_B', K_ESCAPE : 'S'}
                    # print(touches)
                    touche = event.key
                    if touche in touches:
                        return touches[touche]
                    return event.unicode
                
                elif event.type == pygame.VIDEORESIZE:
                    pass
                
                

class Bouton:
    def __init__(self, w, h, nom, w_pol=32):
        self.w = w
        self.h = h
        self.pol = pygame.font.SysFont("Arial Black.ttf", w_pol)
        self.pressed = False
        self._enable = True
        self._visible = True
        self.image = None
        self.setName(nom)
        self.rect = self.image.get_rect()
        
        
    def copy(self, nom=None):
        bp = Bouton(self.w, self.h, '#'.join(self.nom))
        if nom:
            bp.setName(nom)
        bp.rect = self.rect
        return bp

    def enable(self):
        self._enable = True
        self.setImg()
        
    def disable(self):
        self._enable = False
        self.setImg()
        
    def visible(self):
        self._visible = True
        self.enable()
        
    def invisible(self):
        self._visible = False
        self.disable()        

    def setImg(self):
        self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        if self._visible:
            if not self._enable:
                clrCase = COLORBPD
                texte = self.pol.render(self.nom[0], True, COLORTXT)
            elif self.pressed :
                clrCase = COLORBPP
                texte = self.pol.render(self.nom[-1], True, COLORTXT)
            else :
                clrCase = COLORBPR
                texte = self.pol.render(self.nom[0], True, COLORTXT)
            self.image.fill(clrCase)        
            rectTexte = texte.get_rect()
            rectTexte.center = self.image.get_rect().center
            self.image.blit(texte, rectTexte)
    
    def setRect(self, left, top):
        self.rect.left = left
        self.rect.top = top
        
    def setName(self, nom):
        self.nom = nom.split('#') # si deux noms différents pour pressé#relaché le # sépare les noms
        self.setImg()
        # print(self.nom)
        
    def presser(self):
        self.pressed = True
        self.setImg()

    def relacher(self):
        self.pressed = False
        self.setImg()
        
    def isCollide(self, pos):
        return self._enable and self.rect.collidepoint(pos)
    

   
    
    
    
    
    