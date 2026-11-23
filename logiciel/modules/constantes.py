import pygame

# Constante du simulateur modifiable par l'utilisateur
VOLUME_BLOC = 12
PRESSION_INITIALE = 220

# Constantes DECO
INTERVAL_MESURE = 0.1 # seconde
W_DECO = 400
H_DECO = 550
W_BG = 16
H_BG_150 = 150
H_BG_100 = H_BG_150 * 100 // 150
H_BG_80 = H_BG_150 * 80 // 150
D_BG = 3
H_ORDI = 363
W_ECRAN = 268
H_ECRAN = 188
MARGE_1 = 100
MARGE_2 = 65
MARGE_3 = 35
COLOR_ORDI_TEXT = '#EFEFEF'
DPI_PLOT = 100
COLORS_PLOT = ['tomato', 'yellowgreen', 'skyblue', 'goldenrod', 'orchid', 'blueviolet', 'slategray']

# Constantes GUI
# Taille de la fenetre de base
# Toutes les dimensions sont ramenées a cette surface
# elle est ensuite redimensionnée vers l'écran final
W_BASE = 1200
H_BASE = 800
COLOR_FOND = pygame.Color("#4091AF")

LIST_BP_BAS = ['START#STOP', 'FASTER', 'SLOWER', 'AUTO UP', 'UP++', 'UP', 'DOWN', 'DOWN++', 'RESET']
BP_DEC_MDE = 'M-VALUE#TIME'
BP_DEC_EN = 'DÉTAILS DÉCO'
BP_HELP = '?'


WBP = 110
WBP_DECO = 180
WBP_HELP = 40
HBP = 60
DBP = 20
YBP = 700
XBP = DBP
X_BP_HELP = W_BASE - WBP_HELP - 20
Y_BP_HELP = 10

X_SPEED = 30
Y_SPEED = 670

X_PROFIL = 400
Y_PROFIL = 75 # 40

MARGE_MANO = 10
MANO_SCALE_FACTOR = 15

X_HEURE = 650
Y_HEURE = 10

HEURE_INIT = 8

COLORBPR = pygame.Color('#205676')#BB3F3F') # #DFA5A5
COLORBPP = pygame.Color('#153047')
COLORBPD = pygame.Color('#4F4F4F')
COLORTXT = pygame.Color('#FFFFFF')

ASSETS = 'assets'

# Constantes profil
W_PROFIL = 780
H_PROFIL = 600 # 650
Y_SURF_EAU = 30 # 70
X0_DIVER = 50

COLOR_BLUE = ["#131B35", "#153047", "#205676", "#4091AF", "#56ACCC", "#71C1DE", "#9CE9FF"]
COLOR_SPEED = '#FF7F00' # COLOR_BLUE[-2]
COLOR_HEURE = '#FF7F00'

# POLICE_COMPUTER = "SF Digital Readout Heavy Oblique.ttf"
POLICE_COMPUTER_0 = "DSEG7Classic-BoldItalic.ttf"
W_DIGIT_0 = 45 # 90
W_DIGIT_1 = 30 # 60
POLICE_COMPUTER_2 = "slkscr.ttf"
W_DIGIT_2 = 13 # 20
POLICE_SPEED = "nervous_rex.ttf"
W_SPEED = 64
POLICE_HEURE = "DSEG14Modern-BoldItalic.ttf"#DSEG14Classic-BoldItalic.ttf"
W_HEURE = 55