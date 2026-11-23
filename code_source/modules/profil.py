# Grégory Coutable 2025
# Partage sous licence Creative Commons :
# https://creativecommons.org/licenses/by-sa/3.0/fr/
# 
# Version :
# 1.2 : nouelle gestion du temps
# 1.3 : fond defilant
# 1.4 : Préparation pour l'appli standalone

__autor__ = 'Grégory COUTABLE'
__version__ = '1.4'
__date__ = '19/11/2026'
print(f"Affichage du profil de la plongée : version : {__version__}, {__name__}")

import pygame
from pygame.locals import *
from math import pi, sin, cos, radians
from functools import reduce
from random import randint, choice
import os
from modules.constantes import *

pathname = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))

class Profil:
    def __init__(self):
        self.KY_P = 8
        self.delta_x = 5
        self.time_interval = 20
        self.time_last = 0
        
        self.dive_log = [0]
        self.colors_log = [0]
        self.colors = [(0, 255, 0, 255), (255, 127, 0, 255), (255, 0, 0, 255)]
        self.diver = Diver(100)
        self.compteur_cycle = 0
        self.panaches = []
        self.angle = 90

        self.surface = SurfaceEau(8)
        
        self.fond_defilant = FondDefilant()
        
        self.vue_surface = True
        self.plongee_finie = False
        self.img_plot = None
        
    def update(self, d_t, computer, pression_bloc):
        self.angle = 3 * computer.vitesse_remontee_moy()
        if abs(self.angle) > 90:
            self.angle = 90 * self.angle / abs(self.angle)
        
        for p in self.panaches:
            p.update(d_t, computer.prof)
            
        self.fond_defilant.update(d_t)
            
        if self.vue_surface and computer.mode == 1:
            self.vue_surface = False
        
        self.time_last += d_t
        if self.time_last >= self.time_interval:
            self.compteur_cycle += 1
            
            if self.compteur_cycle % 5 == 0:
                x = X0_DIVER + self.delta_x * (len(self.dive_log) - 1) + 40 * cos(radians(self.angle))
                y = Y_SURF_EAU + self.KY_P * computer.prof - 40 * sin(radians(self.angle))
                self.panaches.append(PanacheBulles(x, y, computer.prof))
                # ramasse miette
                for i in range(len(self.panaches) -1, -1, -1):
                    if not self.panaches[i].bulles:
                        del self.panaches[i]

            self.time_last = 0

            if computer.mode in (1, 2):
                self.dive_log.append(computer.prof)
                if computer.deco_dive:
                    self.colors_log.append(2)
                elif computer.no_deco_time < 3:
                    self.colors_log.append(1)
                else:
                    self.colors_log.append(0)
                    
            
            # alarme profondeur et pression
            if round(computer.prof, 1) > [20, 40, 60][self.diver.niveau - 1] + 2 or pression_bloc < 20:
                self.diver.set_alarm(1, self.colors[2])
            elif round(computer.prof, 1) > [20, 40, 60][self.diver.niveau - 1] or pression_bloc < 50:
                self.diver.set_alarm(1, self.colors[1])
            else:
                self.diver.set_alarm(0)
                
            if pression_bloc == 0:
                self.diver.set_alarm(2, self.colors[2])
                
    def visu_deco(self, computer):
        self.plongee_finie = True
        #self.img_plot
        if computer.affiche_compartiments:
            self.image = pygame.transform.smoothscale(pygame.image.load(computer.deco.plot(), 'temp.png'), (W_PROFIL, H_PROFIL))
        else:
            self.image = pygame.transform.smoothscale(pygame.image.load(os.path.join(pathname, ASSETS, "surface2.png")), (W_PROFIL, H_PROFIL))
            
    def get_image(self, d_x=0, anim=True, prof=None):
        if self.vue_surface:
            return pygame.transform.smoothscale(pygame.image.load(os.path.join(pathname, ASSETS, "surface.png")), (W_PROFIL, H_PROFIL))
            
        if anim:
            self.diver.update()
            
        if prof is None:
            prof = self.dive_log[-1]
       
        if self.plongee_finie:
            # self.image = self.img_plot
            return self.image
#             self.image = pygame.Surface((W_PROFIL, H_PROFIL))
#             self.image.fill(pygame.Color(COLOR_BLUE[2]))
        else:
            self.image = self.fond_defilant.get_image(d_x)
        
        if X0_DIVER + self.delta_x * (len(self.dive_log)) > W_PROFIL - 100:
            self.delta_x -= 1
        
        self.surface.draw_surface_eau(self.image)
        
        for i in range(len(self.dive_log)):
            if i == len(self.dive_log) - 1:
                if not self.plongee_finie:
                    prof_current = prof
                    delta_x_px = self.delta_x * (i + self.time_last /self.time_interval)
                else:
                    prof_current = self.dive_log[i]
                    delta_x_px = self.delta_x * i                 
            else:
                prof_current = self.dive_log[i + 1]
                delta_x_px = self.delta_x * (i + 1)
#            pygame.draw.line(self.image, pygame.Color(self.colors[self.colors_log[i]]),
            pygame.draw.line(self.image, self.colors[self.colors_log[i]],
                             (X0_DIVER + self.delta_x * i, Y_SURF_EAU + self.KY_P * self.dive_log[i]),
                             (X0_DIVER + delta_x_px, Y_SURF_EAU + self.KY_P * prof_current), width = 5)
        
        if not self.plongee_finie:
            rot_diver = pygame.transform.rotate(self.diver.image, self.angle)
            rot_rect = rot_diver.get_rect()
            rot_rect.center = (X0_DIVER + self.delta_x * (len(self.dive_log) - 1 + self.time_last /self.time_interval) - 10,
                                      Y_SURF_EAU + self.KY_P * prof)
            self.image.blit(rot_diver, rot_rect)
            
        for p in self.panaches:
            self.image.blit(p.draw(), (0, 0))
        
        return self.image
    
    def get_rect(self):
        return self.image.get_rect()
    
class PanacheBulles:
    def __init__(self, x, y, prof):
        self.bulles = []
        for _ in range(20):
            dx, dy = randint(-5, 5), randint(-5, 5)
            self.bulles.append(Bulle(x + dx, y + dy, prof))
        
    def update(self, d_t, prof):
        for b in self.bulles:
            b.update(d_t, prof)
        # ramasse miette
        for i in range(len(self.bulles) - 1, -1, -1):
            if not self.bulles[i].alive:
                del self.bulles[i]
                
    def draw(self):
        image = pygame.Surface((W_PROFIL, H_PROFIL), pygame.SRCALPHA)
        
        for b in self.bulles:
            b.draw(image)
            
        return image
    
class Bulle:
    def __init__(self, x, y, prof):
        self.x, self.y = x, y
        self.rayon_init = randint(10, 30) / 10
        self.rayon = 0
        self.alive = True
        self.pression_init = prof / 10 + 1
        
    def update(self, d_t, prof):
        pression = prof / 10 + 1
        self.rayon = ((self.rayon_init ** 2) * self.pression_init / pression) ** (1 / 2)
        self.y -= self.rayon * d_t
        if self.y <= Y_SURF_EAU:
            self.alive = False
        
    def draw(self, image):
        rect = pygame.Rect(self.x, self.y, round(self.rayon), round(self.rayon / 2))
        pygame.draw.ellipse(image,
                           pygame.Color(255, 255, 255),
                           rect,
                           width=1)        

class Diver(pygame.sprite.Sprite):
    def __init__(self, width, niveau=3):
        """Instancie un plongeur.

        parametres
        ----------
        width : int
            longueur du plongeur en pixel
        niveau : int 1..3
            Niveau du plongeur 1 -> PA20, 2 -> PA40, 3 -> PA60.
        """
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet_brut = pygame.image.load(os.path.join(pathname, ASSETS, "diver.png")).convert_alpha()
        w_brut, h_brut = sprite_sheet_brut.get_size()
        w_d, h_d = w_brut, h_brut // 10
        self.W_diver = width
        self.H_diver = (h_d * width) // w_d
        
        self.niveau = niveau
        self.alarm_level = 0 # 0 -> pas d'alarme, 1 -> alarme cligotant, 2 -> fixe
        self.alarm_color = (0, 0, 0, 0)

        self.spriteSheet = pygame.transform.scale(sprite_sheet_brut, (self.W_diver, 10 * self.H_diver))

        self.image_b = self.spriteSheet.subsurface(pygame.Rect(0, 0, self.W_diver, self.H_diver))
        self.image = self.image_b
        
        self.rect = self.image.get_rect()

        self.cmpt_dizieme = 0
        self.numeroImage = 0
        
    def set_alarm(self, level, color=(0, 0, 0, 0)):
        self.alarm_color = color
        self.alarm_level = level
           
    def update(self):
        self.image_b = self.spriteSheet.subsurface(pygame.Rect(0,
                                                             self.H_diver * self.numeroImage,
                                                             self.W_diver,
                                                             self.H_diver))
        
        if self.alarm_level == 2 or self.alarm_level == 1 and (self.cmpt_dizieme // 3) % 2 == 0:
            self.image = self.image_unie()
        else:
            self.image = self.image_b
        
        self.numeroImage = (self.numeroImage + 1) % 10
            
    def image_unie(self):
        image = self.image_b.copy()
        
        for x in range(image.get_width()):
            for y in range(image.get_height()):
                if self.image_b.get_at((x, y))[3] < 255:
                    image.set_at((x, y), (0, 0, 0, 0))
                else:
                    image.set_at((x, y), self.alarm_color)
                   
        return image
            
class SurfaceEau:
    def __init__(self, n):
        self.ondul = []
        self.def_pix = 3
        
        for i in range(n):
            amp = [randint(2, 3) for i in range(3)]
            w = 2 * pi / randint(100, 200)
            ph = [randint(5, 20) for i in range(3)]
            
            self.ondul.append([self._get(x, amp, w, ph) for x in range(W_PROFIL // self.def_pix)])
        
    def draw_surface_eau(self, image):
        for j in range(len(self.ondul)):
            ondulations = self.ondul[j]
            for i in range(len(ondulations) - 1):
                pygame.draw.line(image, pygame.Color(COLOR_BLUE[j % len(COLOR_BLUE)]),
                                 (self.def_pix * i, Y_SURF_EAU + ondulations[i]),
                                 (self.def_pix * (i + 1), Y_SURF_EAU + ondulations[i + 1]),
                                 width=2)        
        
    def _get(self, x, amp, w, ph):
        return reduce(lambda acc, i: acc + amp[i] * sin(w * (i + 1) * x + ph[i]), range(len(amp)), 0)

class FondDefilant:
    def __init__(self):
        self.image_fond = pygame.image.load(os.path.join(pathname, ASSETS, "fond_defilant.png")).convert_alpha()
        w, h = self.image_fond.get_size()
        h_subaqua = H_PROFIL - Y_SURF_EAU
        if h != h_subaqua:
            self.image_fond = pygame.transform.smoothscale(self.image_fond, (h_subaqua * w // h, h_subaqua))
            w, h = self.image_fond.get_size()
        self.defilement_max = w - W_PROFIL
        self.bio = [AnimBio('requin_1', 400, 80, 2),
                    AnimBio('tortue', 400, 400, 0.2, 400 - Y_SURF_EAU, -1),
                    AnimBio('banc_1', 0, 300, -2),
                    AnimBio('banc_2', 800, 500, 1),
                    AnimBio('banc_3', 400, 450, -1),
                    AnimBio('meduse_1', 800, 200, 0.1, 100, 0.6),
                    AnimBio('poisson_1', 400, 400, 2)]
        
    def update(self, d_t):
        for b in self.bio:
            b.update(d_t)
        
    def get_image(self, d_x=0):
        d_x = round(d_x)
        if d_x > self.defilement_max:
            d_x = self.defilement_max
            
        fond = pygame.Surface((W_PROFIL, H_PROFIL), pygame.SRCALPHA)
        fond.blit(self.image_fond, (-d_x, Y_SURF_EAU))
        
        for b in self.bio:
            b.draw(fond, d_x)
            
        return fond
        
class AnimBio:
    filename = ['requin_1', 'requin_2', 'requin_3', 'tortue', 'banc_1', 'banc_2', 'banc_3',
                'hyppocampe', 'poisson_1', 'poisson_2', 'meduse_1', 'meduse_2']
    def __init__(self, name, x0, y0, vitesse_horizontale=0, oscillation_verticale=None, vitesse_verticale=0):
        assert name in AnimBio.filename, \
                f'le nom doit figurer dans cette liste : {", ".join(AnimBio.filename)}'
        self.x = x0
        self.y = y0
        self.delta_y = 0
        self.vitesse_horizontale = vitesse_horizontale
        self.vitesse_verticale = vitesse_verticale
        self.oscillation_verticale = oscillation_verticale
        self.sprite = pygame.image.load(os.path.join(pathname, ASSETS, name + '.png')).convert_alpha()
        self.sprite_r = pygame.transform.flip(self.sprite, True, False)
        
    def update(self, d_t):
        self.x -= self.vitesse_horizontale * d_t

        w, _ = self.sprite.get_size()
        if self.x < -w:
            if choice((True, False)):
                self.x = W_PROFIL + w
            else:
                self.vitesse_horizontale *= -1
        elif self.x > W_PROFIL + w:
            if choice((True, False)):
                self.x = 0
            else:
                self.vitesse_horizontale *= -1
                
        if self.oscillation_verticale:        
            self.delta_y += self.vitesse_verticale * d_t
            if self.delta_y >= self.oscillation_verticale:
                self.delta_y = self.oscillation_verticale - 1
                self.vitesse_verticale *= -1
            elif self.delta_y <= 0:
                self.delta_y = 1
                self.vitesse_verticale *= -1        
            
    def draw(self, image, dx):
        pos = (self.x - dx, self.y - self.delta_y)
        if self.vitesse_horizontale >= 0:
            image.blit(self.sprite, pos)
        else:
            image.blit(self.sprite_r, pos)


    
    
    
    
