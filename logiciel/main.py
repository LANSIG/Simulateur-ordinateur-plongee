# Grégory Coutable 2025
# Partage sous licence Creative Commons :
# https://creativecommons.org/licenses/by-sa/3.0/fr/
#
# Version :
# 1.2 : palier de sécu
# 1.3 : GUI dans un module externe
# 2.1 : La classe Computer a basculé vers le module deco. Ajout des alarmes sur le plongeur.
# 2.2 : Nouvelle version du gui ave fenetre redimensionnable. Bouton RESET.
# 3.1 : modification de la gestion du temps
# 3.3 : deco optionnelle. finalisation des affichages des profils
# 3.4 : Préparation pour l'appli standalone

__autor__ = 'Grégory COUTABLE'
__version__ = '3.4'
__date__ = '19/11/2026'
print(f"\nProgramme de simulation d'un ordinateur de plongée : version : {__version__}, {__name__}\n")

import pygame
from pygame.locals import *
import webbrowser
import time
import os
from random import randint
from math import ceil, isclose, floor
pathname = os.path.dirname(__file__)

from modules.deco import Computer
from modules.gui_dive import GUIdive, Bouton
from modules.profil import Profil
from modules.constantes import *

class DivingSimulation:

    
    def __init__(self):
        self.interval_mesure = int(INTERVAL_MESURE * 10) # en dizième de seconde
        
        self.gui = GUIdive()
        self.init_plongee()
        
        self.run()
        
    def init_plongee(self):
        self.gui.init_heure()
        self.computer = Computer()

        self.bloc = Bloc(PRESSION_INITIALE, contenance=VOLUME_BLOC, scale_factor=MANO_SCALE_FACTOR)
        
        self.computer.set_bloc(self.bloc)
        self.gui.set_computer(self.computer)
        self.gui.set_bloc(self.bloc)
        
        self.profil = Profil()
        self.gui.set_profil(self.profil)
        
        self.speed = 10
        
        self.time_dizieme_seconde = 0
        self.enable = False
        
        self.auto_up = False
        # stop_palier indique si on est arrivé aux paliers
        # arrivée au premier palier
        # la vitesse tombe a 6m/min
        self.stop_palier = False
        self.prof_stop_auto = 0

        self.dtr_reelle = 0
        self.remontee = False

    def faster(self):
        match self.speed:
            case 1:
                self.speed = 1.5
            case 1.5:
                self.speed = 2
            case i if i < 10:
                self.speed += 1
            case i if i < 20:
                self.speed += 2
            case i if i < 200:
                self.speed += 10                
            case _:
                pass
        
    def slower(self):
        match self.speed:
            case 1:
                pass
            case 1.5:
                self.speed = 1
            case 2:
                self.speed = 1.5               
            case i if i < 11:
                self.speed -= 1
            case i if i < 30:
                self.speed -= 2
            case _:
                self.speed -= 10                

    def start(self):
        if self.computer.mode == 3:
            self.gui.visible_bp([0, 1, 2, 8, 11] + ([9] if self.computer.affiche_compartiments else []))
        else:
            self.gui.visible_bp(list(range(9)) + [11])
            if not self.computer.affiche_compartiments:
                self.gui.bp[10].visible()
        self.gui.bp[0].presser()
        self.enable = True

    def stop(self):
        self.gui.visible_bp([0, 1, 2, 8, 11] + \
                            ([10] if (not self.computer.affiche_compartiments and self.computer.mode != 3) else []) + \
                            ([9] if (self.computer.affiche_compartiments and self.computer.mode == 3) else []))
        self.gui.bp[0].relacher()
        self.enable = False

    def run(self):
        while True:
            # C'est gui.waitClick(1) qui cadence cette boucle toutes les 100ms
            self.gui.refresh(self.speed, not self.enable)
            
            click = self.gui.waitClick(self.interval_mesure) # attend 1 dizième de seconde
            if isinstance(click, str) and click.startswith('BP'):
                # print(click)
                num = int(click[2:])
                match num:
                    case 0: # START/STOP
                        if self.enable:
                            self.stop()
                        else:
                            self.start()
                        
                    case 1: # FASTER
                        self.faster()
                        
                    case 2: # SLOWER
                        self.slower()

                    case 3: # AUTO UP -> remontée automatique
                        self.remontee = True
                        if self.computer.prof == 3:
                            self.prof_stop_auto = 0
                        else:
                            self.prof_stop_auto = self.computer.prof_premier_palier
                        self.auto_up = True

                    case 4: # UP++
                        self.auto_up = False
                        self.computer.ajoute_prof(-1.0)
                        
                    case 5: # UP
                        self.auto_up = False
                        self.computer.ajoute_prof(-0.1)

                    case 6: # DOWN
                        self.auto_up = False
                        if self.computer.prof < 65:
                            self.computer.ajoute_prof(0.1)
                            self.start()
                        if self.stop_palier and self.computer.prof > 12:
                            self.stop_palier = False
            
                    case 7: # DOWN++
                        self.auto_up = False
                        if self.computer.prof < 65:
                            self.computer.ajoute_prof(1.0)
                            self.start()            
                        if self.stop_palier and self.computer.prof > 12:
                            self.stop_palier = False
                            
                    case 8:
                        self.init_plongee()
                        
                    case 9: # mode affichage profil fin de plongée
                        if self.gui.bp[9].pressed:
                            self.gui.bp[9].relacher()
                            self.computer.deco.set_type_plot(0)
                        else:
                            self.gui.bp[9].presser()
                            self.computer.deco.set_type_plot(1)
                        self.profil.visu_deco(self.computer)
                    
                    case 10: # affiche compartiment
                        self.computer.set_affiche_compartiments()
                        self.gui.bp[10].invisible()
                        
                    case 11: # affiche l'aide du depot github
                        webbrowser.open('https://github.com/LANSIG/Simulateur-ordinateur-plongee/blob/403f21dc3af2c9389e235c687b0a31043999a090/Documentation.md')                    

            if self.computer.mode == 3 and not self.profil.plongee_finie:
                self.profil.visu_deco(self.computer)
                self.gui.visible_bp([0, 1, 2, 8, 11] + ([9] if self.computer.affiche_compartiments else []))

            if self.enable:
                if self.remontee and self.computer.prof <= 0.1:
                    self.remontee = False
                    # print(self.dtr_reelle)
                    
                if self.remontee:
                    self.dtr_reelle += 0.1 * self.speed
                
                if self.auto_up:
#                     self.computer.deco.compartiments[2].init_tn2_palier()
#                     self.computer.deco.compartiments[2].remontee(self.computer.prof, 0)
#                     print('remontee :',
#                           self.computer.prof,
#                           self.computer.deco.compartiments[2].tn2, '->',
#                           self.computer.deco.compartiments[2].tn2_p, '->',
#                           self.computer.deco.compartiments[2].tn2_decollage_avant_palier(self.computer.prof))
                    
                    if self.stop_palier or self.computer.prof_premier_palier >= 3:
                        self.prof_stop_auto = self.computer.prof_premier_palier
                    else :
                        self.prof_stop_auto = 3
                    # remontée de 10m/mn -> 10m en 600dz -> 1/60 m/dz * speed
                    vr_1 = INTERVAL_MESURE * 10 / 60
                    # remontée de 6m/mn -> 6m en 600dz -> 1/100 m/dz * speed
                    vr_2 = INTERVAL_MESURE * 6 / 60
                    delta_prof = (vr_1 if not self.stop_palier and self.computer.prof > 6 else vr_2) * self.speed
                    self.computer.set_prof(self.computer.prof - delta_prof)
                    if self.computer.prof < self.prof_stop_auto:
                        # on vient d'arriver au palier
                        self.computer.set_prof(self.prof_stop_auto)
                        # On abaisse la vitesse de remontée auto
                        self.stop_palier = True
                        self.auto_up = False
                
                self.computer.update(INTERVAL_MESURE * self.speed)
                self.bloc.refresh_gaz(self.computer.prof, INTERVAL_MESURE * self.speed / 60)
                self.profil.update(INTERVAL_MESURE * self.speed,
                                   self.computer,
                                   self.bloc.pression)

class Bloc:
    def __init__(self, pression, contenance=12, gaz='air', scale_factor=100):
        self.gaz = gaz
        self.contenance = contenance
        self.pression = pression
        self.conso = 12 # L/min
        
        img_mano = pygame.image.load(os.path.join(pathname, ASSETS, "mano.png")).convert_alpha()
        w, h = img_mano.get_size()
        self.img_mano = pygame.transform.scale(img_mano, (w * scale_factor // 100, h * scale_factor // 100))

        img_aiguille = pygame.image.load(os.path.join(pathname, ASSETS, "aiguille.png")).convert_alpha()
        w, h = img_aiguille.get_size()
        self.img_aiguille = pygame.transform.scale(img_aiguille, (w * scale_factor // 100, h * scale_factor // 100))
        
    def refresh_gaz(self, prof, d_t):
        """retire du gaz.

        parametres
        ----------
        d_t : int ou float
            interval de temps écoulé depuis la dernière mise a jour du gaz. En minute !!
        prof : float
            profondeur d'utilisation en m
        """
        if prof > 0:
            volume_restant = self.contenance * self.pression - (prof / 10 + 1) * self.conso * d_t
            self.pression = volume_restant / self.contenance
            if self.pression < 0:
                self.pression = 0
                
    def get_image_mano(self):
        mano = self.img_mano.copy()
        size = mano.get_size()
        rot_aig = pygame.transform.rotate(self.img_aiguille, -round(self.pression * 180 / 195))

        rot_rect = rot_aig.get_rect()
        
        rot_rect.center = mano.get_rect().center
        rot_rect.top = rot_rect.top - (size[1] - size[0]) // 2
        
        mano.blit(rot_aig, rot_rect)
        return mano

            
if __name__ == "__main__":
    DivingSimulation()




