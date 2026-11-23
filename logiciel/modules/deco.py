# Grégory Coutable 2025
# Partage sous licence Creative Commons :
# https://creativecommons.org/licenses/by-sa/3.0/fr/
#
# Implémentation d'un simulateur d'ordinateur de plongée
# Inclus un calcul de déco utilisant l'algorithme de Buhlmann
# L'article ayant servi de base à l'impémentation est dispo ici :
# http://www.swiss-cave-diving.ch/PDF-dateien/Elements-calcul-deco_Belin.pdf
# 
# Version :
# 1.1 : Buhlmann ok, TODO : intégrer les remontées
# 1.2 : génération des bargraph
# 2.1 : intègre la classe Computer
# 2.2 : modifs mineures
# 3.1 : modification de la gestion du temps
# 3.3 : mémorisation du profil de charge décharge des compartiments
# 3.4 : prise en charge des remontées dans le calcul des paliers
# 3.5 : affichage des compartiments optionnel
# 3.6 : Préparation pour l'appli standalone

__autor__ = 'Grégory COUTABLE'
__version__ = '3.6'
__date__ = '19/11/2026'

print(f"\nProgramme de modélisation de la déco N2 : version : {__version__}, {__name__}")

import io
from math import log, exp, ceil, floor, isclose
import pygame
from pygame.locals import *
import matplotlib.pyplot as plt
import numpy as np
from modules.constantes import *

#pour le rendre dispo de n'importe où
import os
pathname = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))

class Computer:
    def __init__(self, d_t=20):
        pygame.init()
        
        self.deco = Deco(conserv=100)
        self.police = {}
        self.police['digit_0'] = pygame.font.Font(os.path.join(pathname, ASSETS, POLICE_COMPUTER_0), W_DIGIT_0)
        self.police['digit_1'] = pygame.font.Font(os.path.join(pathname, ASSETS, POLICE_COMPUTER_0), W_DIGIT_1)
        self.police['digit_2'] = pygame.font.Font(os.path.join(pathname, ASSETS, POLICE_COMPUTER_2), W_DIGIT_2)
        self.police['digit_0b'] = pygame.font.Font(os.path.join(pathname, ASSETS, POLICE_HEURE), W_DIGIT_0)
        self.police['arial_0'] = pygame.font.SysFont("Arial Black", round(W_BG * 0.7))
        self.police['arial_1'] = pygame.font.SysFont("Arial", round(W_DECO / 17))
        
        self.icones = {}
        self.icones['descendre'] = pygame.image.load(os.path.join(pathname, ASSETS, "fleche.png")).convert_alpha()
        self.icones['fast'] = pygame.image.load(os.path.join(pathname, ASSETS, "fast.png")).convert_alpha()
        self.icones['paliers'] = pygame.image.load(os.path.join(pathname, ASSETS, "paliers.png")).convert_alpha()
        self.icones['alti'] = pygame.image.load(os.path.join(pathname, ASSETS, "montagne.png")).convert_alpha()
        self.icones['no_fly'] = pygame.image.load(os.path.join(pathname, ASSETS, "no_fly.png")).convert_alpha()
        
        # chagement de couleur des icones
        for img_name in self.icones:
            image = self.icones[img_name]
            for x in range(image.get_width()):
                for y in range(image.get_height()):
                    if image.get_at((x, y))[3] < 200:
                        image.set_at((x, y), (0, 0, 0, 0))
                    else:
                        image.set_at((x, y), pygame.Color(COLOR_ORDI_TEXT))
        # pour mémoire : une autre solution possible
        # mais le résultat est moins beau
#         for img_name in self.icones:
#             img = pygame.PixelArray(self.icones[img_name])
#             img.replace(pygame.Color('#39452D'), pygame.Color(COLOR_ORDI_TEXT), distance=0.1)
        
        self.prof = 0.0
        self.prof_last = 0.0
        self.time_last = 0.0
        self.prof_max = 0
        self.dive_time = 0
        self.periode_calcul_seconde = 5.0
        self.periode_calcul_minute = self.periode_calcul_seconde / 60 # 5s, par défaut -> en minute
        self.defaut_fast = False
        self.defaut_palier = False
        self.enable_palier_secu = False
        self.compte_a_rebourd = 180
        self._time_dz_palier_omis = 0
        self.affiche_compartiments = False
        
        self.paliers = []
        self.palier_omis = False
        self.prof_premier_palier = 3 # fixe l'arret de la remontée automatique
        
        self.enable_no_fly = False
        self.interval_surface = 0
        self.deco_dive = False
        self.no_deco_time = 99
        self.vitesse_verticale = 0
        # demarrage verticale comme en canard
        self.file_vitesse_remontee = [-60] * 20
            
        self.mode = 0  # 0 -> avant, 1 -> pendant, 2 -> arrivée en surface, 3 -> après la plongée
        
        self.bloc = None
        
    def set_affiche_compartiments(self):
        self.affiche_compartiments = True
        
    def vitesse_remontee_moy(self):
        return sum(self.file_vitesse_remontee) / len(self.file_vitesse_remontee)
    
    def _enfile_vitesse(self, v):
        self.file_vitesse_remontee.append(round(v, 1))
        self.file_vitesse_remontee.pop(0)
        # print(self.file_vitesse_remontee, self.vitesse_remontee_moy())

    def set_bloc(self, bloc):
        self.bloc = bloc
        
    def ajoute_prof(self, prof):
        self.set_prof(self.prof + prof)
            
    def set_prof(self, prof):
        if prof >= 0:
            self.prof = prof
        else:
            if prof <= -1 and self.mode == 2:
                # un appui sur up++ a la surface
                # stoppe le compte a rebours time out
                # et arrete l'ordi
                self.compte_a_rebourd = 0.1
            self.prof = 0
            
        if self.prof > self.prof_max:
            self.prof_max = self.prof
        if self.mode == 0 and self.prof >= 1.0:
            self.mode = 1
        elif self.mode == 1 and self.prof < 0.1:
            self.compte_a_rebourd = 180
            self.enable_palier_secu = False
            self.mode = 2
        elif self.mode == 2 and self.prof > 1.0:
            self.mode = 1
            
        if not self.enable_palier_secu and self.prof > 10:
            self.enable_palier_secu = True
            self.enable_no_fly = True

    def update(self, d_t):
        self.time_last += d_t
        
        self.vitesse_verticale = 60 * (self.prof_last - self.prof) / d_t 
        self._enfile_vitesse(self.vitesse_verticale)
        self.prof_last = self.prof
        
        self.defaut_fast = self.vitesse_remontee_moy() >= 13
        
        if self.time_last >= self.periode_calcul_seconde:
            
            periode_calcul_minute = self.time_last / 60
            self.deco.refresh_TN2(self.prof, periode_calcul_minute, self.mode != 3)
            if self.prof > 0.1:
                self.dive_time += periode_calcul_minute
            
            # si la plongée est finie, on maj l'IS
            if self.mode == 3:
                self.interval_surface += periode_calcul_minute
                if self.interval_surface > 1440:
                    self.interval_surface = 0
                    self.mode = 0
                
            self.paliers = self.deco.temps_paliers(self.prof)
            self.prof_premier_palier = len(self.paliers) * 3
            
            if not self.paliers:
                self.no_deco_time = self.deco.no_deco(self.prof)
                
            self.time_last = 0

    def get_image(self, speed, pause):
        """
        Cette méthode renvoi l'image de l'ordinateur.
        
        paramètres
        ----------
        speed : int
            vitesse de défilement de la plongée, > 1, pour *1
        pause : bool
            bloque l'affichage de l'ordi quand la plongée est en pause. Si True, affichage figé
            important pour le décompte du palier de sécu.
        """
        
        self.image = pygame.Surface((W_DECO, H_DECO), pygame.SRCALPHA)

        img_ordi = self._get_ordi()
        rect_ordi = img_ordi.get_rect()
        rect_ordi.center = self.image.get_rect().center
        rect_ordi.top = self.image.get_rect().top
        self.image.blit(img_ordi, rect_ordi)
        if self.affiche_compartiments:
            #self.image.fill(pygame.Color("#00589A"))
            bargraph = self.deco._get_bargraph()
            rect_bargraph = bargraph.get_rect()
            rect_bargraph.center = self.image.get_rect().center
            rect_bargraph.bottom = self.image.get_rect().bottom
            self.image.blit(bargraph, rect_bargraph)            
            
            self._blit_text('arial_1',
                            "Les 16 compartiments de Bühlmann",
                            left=None,
                            top=self.image.get_rect().top + H_ORDI - 30,
                            center=self.image.get_rect().center)
            self._blit_text('arial_1',
                            "Charge N2 / Charge max en % ",
                            left=None,
                            top=self.image.get_rect().top + H_ORDI,
                            center=self.image.get_rect().center)

        match self.mode:
            case 0:
                self._blit_text('digit_0b', "BAT100%", 73, 166)
                self._blit_prof(False)
                
            case 1:
                
                self._blit_prof()
                
                if self.defaut_fast:
                    self._blit_fast()

                else:
                    self._blit_prof_max()
                    
                self._blit_time_gauche('dtime', self.dive_time)
                
                if self.bloc is not None:
                    self._blit_tank()

                if self.paliers:
                    self.deco_dive = True
                    self._blit_paliers()
                    
                    if self.prof < self.prof_premier_palier - 0.3:
                        self._blit_descendre()
                        
                elif self.palier_secu():
                    self.deco_dive = False
                    if self._blit_compte_a_rebourd('safe', speed, pause):
                        self.enable_palier_secu = False
                 
                else:
                    # affichage no deco
                    self._blit_text('digit_0', str(self.no_deco_time) if self.no_deco_time < 99 else "99", 185, 166)
                    self._blit_text('digit_2', 'no deco', 110, 162)         

            case 2:
                self._blit_prof_max()
                self._blit_time_gauche('dtime', self.dive_time)                
                self._blit_prof()
                self._blit_tank()
                if self.deco_dive:
                    self._blit_descendre()
                    
                if self._blit_compte_a_rebourd('time out', speed, pause):
                    self.mode = 3
                    
            case 3:
                self._blit_time_gauche('int surf', self.interval_surface, min_sec=True)
                self._blit_no_fly()
                self._blit_desat()

        if self.deco_dive:
            if self.prof <= self.prof_premier_palier - 1:
                self._time_dz_palier_omis += speed
                
            if self._time_dz_palier_omis >= 1800:
                self.palier_omis = True

        if self.palier_omis:
            self._blit_palier_omis()
            
        self._blit_vitesse()

        return self.image

    def _get_ordi(self):
        img_ordi = pygame.Surface((W_DECO, H_ORDI), pygame.SRCALPHA)
        self._blit_rectangle(img_ordi, (W_ECRAN + MARGE_1, H_ECRAN + MARGE_1), '#303030', MARGE_1 // 2)
        self._blit_rectangle(img_ordi, (W_ECRAN + MARGE_2, H_ECRAN + MARGE_2), '#FFFF00', MARGE_2 // 2)
        self._blit_rectangle(img_ordi, (W_ECRAN + MARGE_3, H_ECRAN + MARGE_3), '#303030', MARGE_3 // 2)
        self._blit_rectangle(img_ordi, (W_ECRAN, H_ECRAN), '#000000')
        y_line_1 = H_ORDI // 2 - H_ECRAN // 6 + 6
        y_line_2 = H_ORDI // 2 + H_ECRAN // 6 + 6
        x_start = W_DECO // 2 - W_ECRAN // 2 + 10
        x_end = W_DECO // 2 + W_ECRAN // 2 - 10
        pygame.draw.line(img_ordi, pygame.Color(COLOR_ORDI_TEXT), (x_start, y_line_1), (x_end, y_line_1), width=2)
        pygame.draw.line(img_ordi, pygame.Color(COLOR_ORDI_TEXT), (x_start, y_line_2), (x_end, y_line_2), width=2)
        return img_ordi

    def _blit_descendre(self):
        rect_fleche = self.icones['descendre'].get_rect()
        rect_fleche.top = 118
        rect_fleche.left = 165 if self.prof < 10 else 195
        self.image.blit(self.icones['descendre'], rect_fleche)

    def _blit_fast(self):
        self._blit_text('digit_1', 'FAST', 235, 118, pygame.Color(COLOR_ORDI_TEXT))
        rect_fleche = self.icones['fast'].get_rect()
        rect_fleche.top = 118
        rect_fleche.left = 212
        self.image.blit(self.icones['fast'], rect_fleche)
        
    def _blit_rectangle(self, img_ordi, dimension, color, rayon_coin=0):
        rect_cadre = Rect(0, 0, *dimension)
        rect_ordi = img_ordi.get_rect()
        rect_cadre.center = rect_ordi.center
        pygame.draw.rect(img_ordi, pygame.Color(color), rect_cadre,
                         border_top_left_radius=rayon_coin, border_top_right_radius=rayon_coin,
                         border_bottom_left_radius=rayon_coin, border_bottom_right_radius=rayon_coin)

    def _blit_barre(self, w, h, x, y, color):
        rect_cadre = Rect(0, 0, w, h)
        rect_cadre.left = x
        rect_cadre.bottom = y
        pygame.draw.rect(self.image, pygame.Color(color), rect_cadre)
        
    def _blit_vitesse(self):
        v_max = 14
        v_seuil_1 = 10
        v_seuil_2 = 12
        # indicateur de vitesse
        h_0 = H_ECRAN * v_seuil_1 // v_max
        h_1 = H_ECRAN * (v_seuil_2 - v_seuil_1) // v_max
        h_2 = H_ECRAN - h_0 - h_1
        x = (W_DECO - W_ECRAN) // 2 - 10
        y0 = (H_ORDI + H_ECRAN) // 2
        w_bar = 5
        
        self._blit_barre(w_bar, h_0, x, y0, pygame.Color('#00FF00'))
        self._blit_barre(w_bar, h_1, x, y0 - h_0, pygame.Color('#FFFF00'))
        self._blit_barre(w_bar, h_2, x, y0 - h_0 - h_1, pygame.Color('#FF0000'))
        
        vitesse_verticale = self.vitesse_remontee_moy()
        if vitesse_verticale <= 0:
            return
        
        h = H_ECRAN * (vitesse_verticale if vitesse_verticale < v_max else v_max) / v_max
        w_bar = 8
        self._blit_barre(w_bar, h, x + 10, y0, pygame.Color(COLOR_ORDI_TEXT))

    def _blit_paliers(self):
        duree_premier_palier = self.paliers[0] if len(self.paliers) > 0 else 0
        asc_time = ceil(sum(self.paliers) + 0.5 * len(self.paliers) + self.prof / 10)
    #             print(paliers, asc_time, no_deco_time)
        self._blit_text('digit_1', str(self.prof_premier_palier), 90 if self.prof_premier_palier < 10 else 68, 178)
        self._blit_text('digit_2', 'deco', 135, 162)
        self._blit_text('digit_2', 'm', 120, 201)
        self._blit_text('digit_0', f"{duree_premier_palier}:", 170, 166)
        self._blit_text('digit_2', 'asc', 300, 162)
        self._blit_text('digit_1', f"{asc_time}:", 281 if asc_time < 10 else 261, 178)

    def palier_secu(self):
        if self.enable_palier_secu:
            if self.compte_a_rebourd == 180 and self.prof < 5:
                # entrée dans le palier de sécu
                return True
            if self.compte_a_rebourd < 180 and 2 < self.prof < 6:
                # maintient dans le palier de sécu
                return True
        return False
    
    def _blit_desat(self):                
        desat_time = self.deco.desat_time()
        if desat_time > 0:
            self._blit_time_gauche('desat', desat_time, min_sec=True, bas=False, dx=-10)
            rect_alti = self.icones['alti'].get_rect()
            rect_alti.top = 122
            rect_alti.left = 168
            self.image.blit(self.icones['alti'], rect_alti)    
    
    def _blit_palier_omis(self):
        rect_paliers = self.icones['paliers'].get_rect()
        rect_paliers.top = 100
        rect_paliers.left = 200
        self.image.blit(self.icones['paliers'], rect_paliers)

    def _blit_time_gauche(self, txt, time, min_sec=False, bas=True, dx=0):
        time = int(time)
        if bas:
            y0 = 217
        else:
            y0 = 100
            
        x0 = 75 + dx
        
        if min_sec:
            sec = time % 60
            time = time // 60
            #self._blit_text('digit_1', ('0' if sec < 10 else '') + str(sec), x0 + 55, y0 + 20)
            
        self._blit_text('digit_1', f"{time}:{'0' if min_sec and sec < 10 else ''}{sec if min_sec else ''}",
                        x0 + 20 if time < 10 else x0, y0 + 18)
        self._blit_text('digit_2', txt, x0 + 10, y0 + 5)

    def _blit_tank(self):
        self._blit_text('digit_1', str(int(self.bloc.pression)), 242, 235)
        self._blit_text('digit_2', 'b', 314, 258)
        self._blit_text('digit_2', 'tank', 250, 222)        
                
    def _blit_prof_max(self):
        self._blit_text('digit_2', 'max', 275 if self.prof_max < 10 else 255, 101)
        self._blit_text('digit_1', str(round(self.prof_max, 1)), 270 if self.prof_max < 10 else 248, 120)

    def _blit_text(self, pol, text, left, top, color=pygame.Color(COLOR_ORDI_TEXT), center=None):
        txt = self.police[pol].render(text, True, color)
        txt_rect = txt.get_rect()
        if center is not None:
            txt_rect.center = center
        if left is not None:
            txt_rect.left = left
        txt_rect.top = top
        self.image.blit(txt, txt_rect)        

    def _blit_prof(self, on=True):
        prof_aff = self.prof
        if not on or self.prof < 0.1:
            self._blit_text('digit_0', '-.-', 75, 105)
        else:
            self._blit_text('digit_0', str(round(float(prof_aff), 1)), 75, 105)
        self._blit_text('digit_2', 'm', 155 if prof_aff < 10 else 190, 142)

    def _blit_compte_a_rebourd(self, txt, speed, pause=False):
        secondes = int(self.compte_a_rebourd) % 60
        self._blit_text('digit_1', f"{int(self.compte_a_rebourd) // 60}:{'0' if secondes < 10 else ''}{secondes}", 150, 177)
        self._blit_text('digit_2', txt, 138, 162)
         
        if not pause:
            if self.compte_a_rebourd > 0:
                # un dizième de seconde écoulé dans le monde réel.
                # self.speed dizièmes de secondes dans la plongée
                self.compte_a_rebourd -= 0.1 * speed
                return False
            else:
                self.compte_a_rebourd = 180
                return True
        return False
    
    def _blit_no_fly(self):
        rect_no_fly = self.icones['no_fly'].get_rect()
        rect_no_fly.top = 127
        rect_no_fly.left = 235
        self.image.blit(self.icones['no_fly'], rect_no_fly)
        
        no_fly_time = ceil(24 - self.interval_surface / 60)
        self._blit_text('digit_2', 'no fly', 270, 101)
        self._blit_text('digit_1', str(no_fly_time), 263, 115)
        self._blit_text('digit_2', "h", 315, 115)

class Compartiment:
    # unité : la minute
    PERIODE = [5, 8, 12.5, 18.5, 27, 38.3, 54.3, 77, 109, 146, 187, 239, 305, 390, 498, 635]
    M0 = [2.96, 2.54, 2.25, 2.03, 1.9, 1.75, 1.65, 1.57, 1.52, 1.46, 1.42, 1.39, 1.34, 1.32, 1.29, 1.27]
    DELTA_M = [1.7928, 1.5352, 1.3847, 1.278, 1.2306, 1.1857, 1.1504, 1.1223, 1.0999, 1.0844, 1.0731, 1.0635, 1.0552, 1.0478, 1.0414, 1.0359]
    
    def __init__(self, n, conserv, tn2i=0.8):
        """

        parametres
        ----------
        n : int
            Numéro du compartiment
        """
        assert 0 <= n <= 15, 'Numéro de compartiment de 0 à 15'
        self.n = n
        self.tn2 = tn2i
        self.tn2_p = tn2i # pour prévision des paliers
        
        # calcul de la droite des M-values en incluant le conservatisme
        self.periode = Compartiment.PERIODE[n]
        self.M0 = 1 + (Compartiment.M0[n] - 1) * conserv / 100
        self.delta_M = 1 + (Compartiment.DELTA_M[n] - 1) * conserv / 100
        
        self.t = 0
        self.t_x = [0]
        self.tn2_y = [tn2i]
        self.pabs_y = [1]

    def init_tn2_palier(self):
        self.tn2_p = self.tn2
        
    @staticmethod
    def prof2pabs(prof):
        # eau douce
        return 1 + prof / 10
    
    @staticmethod
    def pabs2prof(pabs):
        # eau douce
        return (pabs - 1) * 10

    @staticmethod
    def prof2ppN2(prof):
        # air
        return 0.8 * Compartiment.prof2pabs(prof)
    
    def refresh_TN2(self, prof, d_t=1, log=True):
        self.t += d_t
        self.tn2 = self.equa_diff(self.prof2ppN2(prof), self.tn2, d_t)
        if log:
            self.t_x.append(self.t)
            self.tn2_y.append(self.tn2)
            self.pabs_y.append(self.prof2pabs(prof))

    def remontee(self, prof_depart, prof_finale, vitesse=10):
        # fait remontée le tn2 fictif (calcul palier)
        # ajout de la remontée a self.tn2_p
        self.tn2_p = self._schreiner(prof_depart, prof_finale, self.tn2_p, vitesse)

    def _schreiner(self, prof_depart, prof_finale, tn2_depart, vitesse=10):
        # équation de Schreiner
        # unités : metre, bar et minute
        ppN2i = self.prof2ppN2(prof_depart)
        t_montee = (prof_depart - prof_finale) / vitesse
        # taux de variation de la pression d'azote dans le gaz inspiré bar / minute
        R = -0.8 * vitesse / 10
        # tn2_final
        return ppN2i + R * (t_montee - self.periode / log(2))  - (ppN2i - tn2_depart - R * self.periode / log(2)) * 2**(-t_montee / self.periode)

    def _schreiner_renverse(self, prof_depart, prof_finale, tn2_final, vitesse=10):
        # équation de Schreiner
        # a l'envers: permet de calculer le tn2_depart avant la montée a vitesse constante pour obtenir le tn2_final
        # unités : metre, bar et minute
        ppN2i = self.prof2ppN2(prof_depart)
        t_montee = (prof_depart - prof_finale) / vitesse
        # taux de variation de la pression d'azote dans le gaz inspiré bar / minute
        R = -0.8 * vitesse / 10      
        tn2_depart = (tn2_final - ppN2i - R * (t_montee - self.periode / log(2))) * 2**(t_montee / self.periode) + (ppN2i - R * self.periode / log(2))
        return tn2_depart
    
    def tn2_decollage_avant_palier(self, prof_depart, prof_palier_suivant=0):
        """
        Vitesse de remontée : 10m/min jusqu'à 3m de l'arrivée, puis, 6m/min
        """
        delta_prof = prof_depart - prof_palier_suivant
        
        if delta_prof <= 3:
            return self._schreiner_renverse(prof_depart, prof_palier_suivant, self.M_value(prof_palier_suivant), vitesse=6)
        
        tn2_3m = self._schreiner_renverse(prof_palier_suivant + 3, prof_palier_suivant, self.M_value(prof_palier_suivant), vitesse=6)
        return self._schreiner_renverse(prof_depart, prof_palier_suivant + 3, tn2_3m, vitesse=10)

    def plot(self):
        plt.plot(self.t_x, self.pabs_y)
        plt.plot(self.t_x, self.tn2_y)
        plt.plot(self.t_x, [self.M_value(0)] * len(self.t_x))
        plt.ylabel(f'tn2 Compartiment N°{self.n}')
        plt.xlabel('time (mn)')
        plt.show()        
        
    def equa_diff(self, ppN2, tn2i, d_t):
        """
        return
        ------
        float
            tn2 atteint en fin d'intervale d_t en respirant ppN2
        """
        return ppN2 + (tn2i - ppN2) * 2**(-d_t / self.periode)

    def equa_diff_inv(self, ppN2, tn2i, tn2f):
        """
        return
        ------
        float
            temps pour passer de tn2i a tn2f en respirant ppN2
        """
        return -log((tn2f - ppN2) / (tn2i - ppN2)) * self.periode / log(2)
    
    def plafond(self, prof_actuelle):
        plafond_target = -3
        tn2_max = 0
        
        while self.tn2 > tn2_max:
            plafond_target += 3
            tn2_max = self.tn2_decollage_avant_palier(prof_actuelle, plafond_target)
            
        return plafond_target
    
    def M_value(self, prof):
        """Calcul du tn2 max a une profondeur donnée.

        return
        ------
        float
            tn2 a ne pas dépasser selon Bulhmann
        """
        return self.delta_M * (self.prof2pabs(prof) - 1) + self.M0
        
    def temps_palier(self, prof):
        # calcul du tn2 a atteindre en fin de palier
        tn2_max = self.tn2_decollage_avant_palier(prof, prof - 3)
        if self.tn2_p > tn2_max:
            # calcul du temps pour y arriver
            return self.equa_diff_inv(self.prof2ppN2(prof), self.tn2_p, tn2_max)
        return 0

    def execute_palier(self, prof, t_palier):
        self.tn2_p = self.equa_diff(self.prof2ppN2(prof), self.tn2_p, t_palier)
        # prise en compte de la remontée vers le palier suivant
        self.remontee(prof, prof - 3, vitesse=6)

    def no_deco(self, prof):
        # tn2 -> tn2_max -> ppn2 : charge avant palier : calcul no_deco
        # tn2 -> ppn2 -> tn2_max : charge avant palier : pas de palier possibles 999
        # ppn2 -> tn2_max -> tn2 : décharge avec palier -1
        # ppn2 -> tn2 -> tn2_max : décharge sans palier 999
        # tn2_max -> ppn2 -> tn2 : décharge avec palier -1
        # tn2_max -> tn2 -> ppn2 : décharge avec palier -1
        tn2_max = self.tn2_decollage_avant_palier(prof, 0)
        ppn2 = self.prof2ppN2(prof)
        if self.tn2 >= tn2_max:
            # palier !!
            return -1
        if ppn2 <= tn2_max:
            # deco ou zone safe
            return 999
        return floor(self.equa_diff_inv(self.prof2ppN2(prof), self.tn2, tn2_max))
    
    def tn2_rel(self):
        return round(100 * (self.tn2) / (self.M_value(0)), 1)

    def desat_time(self):
        ppn2 = 0.8
        if self.tn2 <= 0.83:
            return 0
        return round(self.equa_diff_inv(0.8, self.tn2, 0.83))

class Deco:
    def __init__(self, conserv=100):
        pygame.init()
        self.compartiments = [Compartiment(i, conserv) for i in range(16)]
        self.police = pygame.font.SysFont("Arial Black", 15)
        
        self.histo_declenchement_palier = {}
        self.histo_stop_palier = {}
        self.correspondance_palier_compartiment = {}
        self.type_plot = 0
        
    def set_type_plot(self, mode):
        assert mode in (0, 1)
        self.type_plot = mode
        
    def get_charge_compartiments(self):
        return [c.tn2_rel() for c in self.compartiments]
        
    def refresh_TN2(self, prof, d_t=1, log=True):
        for c in self.compartiments:
            c.refresh_TN2(prof, d_t, log)
            
    def plafond(self, prof_actuelle):
        return max([c.plafond(prof_actuelle) for c in self.compartiments])
    
    def no_deco(self, prof):
        return min([c.no_deco(prof) for c in self.compartiments])
    
    def desat_time(self):
        n_d = max([c.desat_time() for c in self.compartiments])
        return n_d  
    
    def temps_paliers(self, prof_actuelle):
        # prof palier le plus profond
        plafond = self.plafond(prof_actuelle)
        if plafond == 0:
            # les paliers sont terminés
            # détection de la fin du dernier palier (3m)
            if self.correspondance_palier_compartiment and 3 not in self.histo_stop_palier:
                num_comp = self.correspondance_palier_compartiment[3]
                self.histo_stop_palier[3] = (num_comp,
                                            self.compartiments[num_comp].t,
                                            self.compartiments[num_comp].tn2_y[-1])
            return []
        
        prof_paliers = list(range(plafond, -1, -3))
        duree_paliers = [0] * (len(prof_paliers) - 1)
        
        # test si un palier est fini
        if len(prof_paliers) == len(self.correspondance_palier_compartiment):
            p = max(self.correspondance_palier_compartiment.keys())
            num_comp = self.correspondance_palier_compartiment[p]
            self.histo_stop_palier[p] = (num_comp,
                                        self.compartiments[num_comp].t,
                                        self.compartiments[num_comp].tn2_y[-1])
        
        for c in self.compartiments:
            c.init_tn2_palier()
            # remontée au premier palier
            c.remontee(prof_actuelle, prof_paliers[0], vitesse=10)
            
        self.correspondance_palier_compartiment = {}
        for i in range(len(duree_paliers)):
            t_paliers = [c.temps_palier(prof_paliers[i]) for c in self.compartiments]
            d_p_i = max(t_paliers)
            num_comp = t_paliers.index(d_p_i)
            self.correspondance_palier_compartiment[prof_paliers[i]] = num_comp
            duree_paliers[i] = ceil(d_p_i)
            if prof_paliers[i] not in self.histo_declenchement_palier:
                self.histo_declenchement_palier[prof_paliers[i]] = (num_comp,
                                                                    self.compartiments[num_comp].t,
                                                                    self.compartiments[num_comp].tn2_y[-1])
            #print(f'palier {duree_paliers[i]}mn à {prof_paliers[i]}m, compartiment déclencheur {t_paliers.index(d_p_i)}')
            # execution du palier
            for c in self.compartiments:
                c.execute_palier(prof_paliers[i], duree_paliers[i])      
        
        return duree_paliers        

    def _get_bargraph(self):
        #mise a l'echelle des valeurs
        comp_tn2 = [H_BG_150 * charge // 150 for charge in self.get_charge_compartiments()]
        w = (W_BG + 2 * D_BG) * 16
        bargraph = pygame.Surface((w, H_BG_150), pygame.SRCALPHA)
        
        #bargraph.fill(pygame.Color("#0000FF"))
        for i in range(16):
            bar_v = pygame.Surface((W_BG, comp_tn2[i] if comp_tn2[i] <= H_BG_80 else H_BG_80))
            bar_v.fill(pygame.Color("#00FF00"))
            police = pygame.font.SysFont("Arial Black", round(W_BG * 0.7))
            texte = police.render(str(i + 1), True, pygame.Color('#000000'))
            #Une surface pour centrer le texte sur le bandeau du haut
            txt_rect = texte.get_rect()
            txt_rect.center = bar_v.get_rect().center
            txt_rect.bottom = bar_v.get_rect().bottom
            bar_v.blit(texte, txt_rect)
            bargraph.blit(bar_v, ((2*i + 1) * D_BG + i * W_BG,
                                  H_BG_150 - (comp_tn2[i] if comp_tn2[i] <= H_BG_80 else H_BG_80)))
            if comp_tn2[i] > H_BG_80:
                bar_o = pygame.Surface((W_BG, (comp_tn2[i] if comp_tn2[i] <= H_BG_100 else H_BG_100) - H_BG_80))
                bar_o.fill(pygame.Color("#FFFF00"))
                bargraph.blit(bar_o, ((2*i + 1) * D_BG + i * W_BG,
                                      H_BG_150 - (comp_tn2[i] if comp_tn2[i] <= H_BG_100 else H_BG_100)))
            if comp_tn2[i] > H_BG_100:
                bar_r = pygame.Surface((W_BG, (comp_tn2[i] if comp_tn2[i] <= H_BG_150 else H_BG_150) - H_BG_100 ))
                bar_r.fill(pygame.Color("#FF0000"))
                bargraph.blit(bar_r, ((2*i + 1) * D_BG + i * W_BG,
                                      H_BG_150 - (comp_tn2[i] if comp_tn2[i] <= H_BG_150 else H_BG_150)))
                
        self._tracer_ligne(bargraph, H_BG_150 - H_BG_100, pygame.Color('red'), '100%')
        self._tracer_ligne(bargraph, H_BG_150 - H_BG_80, pygame.Color('yellow'), '80%')
        
        return bargraph
    
    def _tracer_ligne(self, bargraph, y, color, text):
        n = 41
        w = (W_BG + 2 * D_BG) * 16
        w_t = w / n
        for i in range(0, n, 2):
            pygame.draw.line(bargraph, color, (i * w_t, y), ((i + 1) * w_t, y), width=2)
        
        txt = self.police.render(text, True, color)
        txt_rect = txt.get_rect()
        txt_rect.right = w
        txt_rect.bottom = y + 2
        bargraph.blit(txt, txt_rect)

    def _trace_graduation(self, ax, x_amp, y_amp, enable_x_tick=True):
        ax.tick_params(axis='both', colors='white')
        ax.grid(which='both')
        ax.grid(which='minor', alpha=0.1)
        ax.tick_params(axis='both', which='minor', length=4, color='white')

        x_min, x_max = x_amp
        y_min, y_max = y_amp
        if enable_x_tick:
            grid_x_ticks = np.arange(x_min, x_max, 0.1)
            ax.set_xticks(grid_x_ticks, minor=True)
        grid_y_ticks = np.arange(y_min, y_max, 0.1)        
        ax.set_yticks(grid_y_ticks, minor=True)
        
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

    def plot(self):
        plt.figure(figsize=(W_PROFIL / DPI_PLOT, W_PROFIL / DPI_PLOT), facecolor=COLOR_BLUE[2])
        ax = plt.gca()  # get current axes
        
        # sélection des compartimesnt à afficher
        cmpt = []
        for c in list(self.histo_declenchement_palier.values()) + list(self.histo_stop_palier.values()):
            if c[0] not in cmpt:
                cmpt.append(c[0])
        cmpt = cmpt if cmpt else [0]
        
        plt.ylabel(f'tn2 Compartiments', color='white')

        if self.type_plot == 0:
            plt.title(f"Evolution de la charge des compartiments {', '.join([str(c) for c in cmpt])}.", color='white')
            plt.xlabel('temps (mn)', color='white')
            
            pabs_max = max(self.compartiments[0].pabs_y) + 0.2
            t_max = self.compartiments[0].t_x[-1]
            self._trace_graduation(ax, (0, t_max), (0, pabs_max), False)            
            
            plt.plot(self.compartiments[0].t_x, self.compartiments[0].pabs_y, color=COLOR_BLUE[1], linewidth=3)
            
            for n in cmpt:
                plt.plot(self.compartiments[n].t_x,
                         self.compartiments[n].tn2_y, color=COLORS_PLOT[n % len(COLORS_PLOT)],
                         label=f"C{n}: {Compartiment.PERIODE[n]}min")

            for p in self.histo_declenchement_palier:
                self._plot_palier_t(p, self.histo_declenchement_palier[p])
            for p in self.histo_stop_palier:
                self._plot_palier_t(p, self.histo_stop_palier[p], declenchement=False)

            # affichage de la légende en bas à droite
            ax.legend(loc='upper right', bbox_to_anchor=(0.99, 0.99), borderaxespad=0.)  


        elif self.type_plot == 1:
            plt.title(f"Diagramme des M-values des compartiments {', '.join([str(c) for c in cmpt])}.", color='white')
            plt.xlabel('Pabs', color='white')
            
            pabs_max = max(self.compartiments[0].pabs_y) + 0.2
            tn2_max = max(self.compartiments[0].tn2_y) + 0.2
            self._trace_graduation(ax, (0, pabs_max), (0, tn2_max))
            
            plt.plot([0, pabs_max], [0, pabs_max], color='black', linewidth=3)
            
            plt.plot([1, 1], [0, pabs_max],
                     color='black', linewidth=1, linestyle='dashed')
            ax.annotate('Surface 0m',
                    xy=(1, ax.get_ylim()[1] - pabs_max / 100),   # ancré en haut du trait
                    xytext=(-2, 0),                    # décalage : 5 points vers la gauche
                    textcoords='offset points',
                    rotation=90,                       # texte vertical
                    va='top',                          # le texte commence en haut (descend)
                    ha='right',                        # collé à gauche du trait
                    color='black', fontsize=10)             

          
            for n in cmpt:
                plt.plot(self.compartiments[0].pabs_y,
                         self.compartiments[n].tn2_y,
                         color=COLORS_PLOT[n % len(COLORS_PLOT)], label=f"C{n}: {Compartiment.PERIODE[n]}min")
                plt.plot([0, pabs_max],
                         [self.compartiments[n].M_value(Compartiment.pabs2prof(0)),
                          self.compartiments[n].M_value(Compartiment.pabs2prof(pabs_max))],
                         '--',
                         color=COLORS_PLOT[n % len(COLORS_PLOT)])
                
            print(self.histo_declenchement_palier)
            print(self.histo_stop_palier)
            for p in self.histo_declenchement_palier:
                n, x, y = self.histo_declenchement_palier[p]
                j = self.compartiments[n].t_x.index(x)
                plt.scatter([self.compartiments[n].pabs_y[j]], [y], color=COLORS_PLOT[n % len(COLORS_PLOT)], s=50, marker='o')
                plt.text(self.compartiments[n].pabs_y[j] - 0.2, y, f'Déclenchement du palier {p}m',
                         color=COLORS_PLOT[n % len(COLORS_PLOT)],
                         horizontalalignment='right')
                
                # Affichage des droites verticales : pression abs au prof de palier
                pabs_plafond = Compartiment.prof2pabs(p)
                plt.plot([pabs_plafond, pabs_plafond], [0, pabs_max],
                         color='black', linewidth=1, linestyle='dashed')
                ax.annotate(f'Profondeur {p}m',
                        xy=(pabs_plafond, ax.get_ylim()[1] - pabs_max / 100),   # ancré en haut du trait
                        xytext=(-2, 0),                    # décalage : 5 points vers la gauche
                        textcoords='offset points',
                        rotation=90,                       # texte vertical
                        va='top',                          # le texte commence en haut (descend)
                        ha='right',                        # collé à gauche du trait
                        color='black', fontsize=10)                
                
#                 plt.scatter([Compartiment.prof2pabs(p - 3)],
#                             [self.compartiments[n].M_value(p - 3)],
#                             color=COLORS_PLOT[n % len(COLORS_PLOT)],
#                             s=50, marker='*')                
#                 plt.text(Compartiment.prof2pabs(p - 3), self.compartiments[n].M_value(p - 3) + 0.1, f'Limite M-value {p - 3}m',
#                          color=COLORS_PLOT[n % len(COLORS_PLOT)],
#                          horizontalalignment='center')                
            
            for p in self.histo_stop_palier:
                n, x, y = self.histo_stop_palier[p]
                j = self.compartiments[n].t_x.index(x)
                plt.scatter([self.compartiments[n].pabs_y[j]], [y], color=COLORS_PLOT[n % len(COLORS_PLOT)], s=50, marker='o')
                plt.text(self.compartiments[n].pabs_y[j] + 0.2, y, f'Fin du palier {p}m', color=COLORS_PLOT[n % len(COLORS_PLOT)])
        
            # affichage de la légende en bas à droite
            ax.legend(loc='lower right', bbox_to_anchor=(0.99, 0.01), borderaxespad=0.)  
        
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='PNG')
        plt.close()  # Fermer la figure pour libérer la mémoire
        buf.seek(0)
        
        return buf

    def _plot_palier_t(self, p, palier, declenchement=True):
        n, x, y = palier
        j = self.compartiments[n].t_x.index(x)
        plt.scatter([x], self.compartiments[n].tn2_y[j], color=COLORS_PLOT[n % len(COLORS_PLOT)], s=50, marker='o')
        plt.text(x, self.compartiments[n].tn2_y[j] - 0.1, f"{'↑' if declenchement else '↓'} palier {p}m",
                 color=COLORS_PLOT[n % len(COLORS_PLOT)],
                 horizontalalignment='center',
                 verticalalignment='top')
        # 'left' if declenchement else 'right'
#         limite_m_value = self.compartiments[n].M_value(p - 3)
#         plt.plot([x - 3, x + 0.5], [limite_m_value, limite_m_value], '--', color=COLORS_PLOT[n % len(COLORS_PLOT)]) 
#         plt.text(x - 2, limite_m_value, f'M-value {p - 3}m',
#                  color=COLORS_PLOT[n % len(COLORS_PLOT)],
#                  horizontalalignment='right',
#                  verticalalignment='bottom')        

if __name__ == '__main__':
#     c1 = Compartiment(3)
#     
#     print(c1.prof2pabs(40))
#     print(c1.prof2ppN2(40))
#     print(c1.tn2)
#     for i in range(160):
#         c1.refresh_TN2(40)
#         print(i, round(c1.tn2, 3), f'{c1.tn2_rel()}%', round(c1.plafond(), 1), c1.paliers() if c1.paliers() else c1.no_deco(40))

#     deco = Deco(conserv=95)
#     
#     for i in range(66):
#         deco.refresh_TN2(25, 1)
#         print(i)
#         print([c.tn2_rel() for c in deco.compartiments])
#         print('plafond :', deco.plafond())
#         print('no deco time', deco.no_deco(40))
#         print(deco.temps_paliers())
#         print()

    deco = Deco(conserv=90)
    deco.refresh_TN2(25, 65)
    print([round(c.tn2, 2) for c in deco.compartiments])
    print(deco.temps_paliers())
    
    deco = Deco(conserv=90)
    for i in range(65):
        deco.refresh_TN2(25, 1)
    print([round(c.tn2, 2) for c in deco.compartiments])
    print(deco.temps_paliers())
    
    deco = Deco(conserv=90)
    for i in range(650):
        deco.refresh_TN2(25, 0.1)
    print([round(c.tn2, 2) for c in deco.compartiments])
    print(deco.temps_paliers())
    
#     ordi = Computer()