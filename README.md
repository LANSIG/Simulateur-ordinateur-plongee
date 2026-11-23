# Simulateur d'ordinateur de plongée

**Auteur : Grégory COUTABLE**
**Copyright © 2026**

***Version 3.4***

## Présentation

Ce projet est un simulateur pédagogique d'ordinateur de plongée. Il permet de visualiser et d'étudier, hors de l'eau, le comportement d'un ordinateur de plongée, notamment à travers la simulation de profils d'immersion et le calcul de décompression basé sur le modèle de **Bühlmann** (1924-1994) avec ses seize compartiments.

Il s'agit avant tout d'un outil de découverte, d'expérimentation et d'apprentissage.

## Avertissement important — Usage exclusivement pédagogique

**Ce logiciel ne doit en aucun cas être utilisé pour préparer, planifier ou conduire une plongée réelle.**

Les calculs et les simulations proposés ne constituent pas une aide à la décision pour la pratique de la plongée. Ils ne remplacent ni un ordinateur de plongée certifié, ni les procédures de sécurité, ni les recommandations d'un organisme de formation.

L'auteur décline toute responsabilité en cas d'utilisation de ce logiciel dans le cadre d'une plongée réelle.

## Exécutable

Un exécutable pour windows est disponible :

https://github.com/LANSIG/Simulateur-ordinateur-plongee/releases/tag/v3.4

Il suffit de le télécharger et de l'exécuter, il est 100% portable et ne nécessite aucune installation. Il a été créé avec `pyinstaller` et peut injustement nécessiter un contrôle supplémentaire de votre anti-virus.

## Documentation

### Avant la plongée

<img src=img/img_1.png width="600px" />

Avant la plongée, l'ordinateur indique le niveau de la batterie.

> [!NOTE]
>
> ***Actions possibles :***
>
> - **FASTER, SLOWER** : Permet de régler la vitesse de la simulation. en *X10*, une plongée de 40mn sera simuler en 4mn. Ce paramètre est également réglable **pendant la plongée**.
> - **DOWN++** : La plongée démarre par une immersion de 1m.

### Pendant la plongée

<img src=img/img_2.png width="600px" />

#### Affichage de l'ordinateur avant palier :

<img src=img/img_6.png width="300px" />

- **PROFONDEUR** : en m.
- **MAX** : Profondeur maximale atteinte en m.
- **DTIME** : Durée de la plongée en minute.
- **TANK** : Pression dans le bloc en bar.
- **NO DECO** : Temps avant palier a cette profondeur.

#### Après enclenchement du premier palier :

<img src=img/img_7.png width="300px" />

- **ASC** : Durée totale de remontée, y compris les paliers obligatoires. Le palier de confort n'est pas inclus dans ce temps.
- **DECO** : Temps et profondeur du premier palier (le plus profond).

> [!NOTE]
>
> ***Actions possibles :***
>
> - **START / STOP** : Permet de mettre en pause ou reprendre la simulation.
> - **DOWN, UP** : montée et descente lente du plongeur : Chaque appui modifiera la **profondeur de 0.1m**.
> - **DOWN++, UP++** : montée et descente rapide du plongeur : Chaque appui modifiera la **profondeur de 1m**. La touche **UP++** permet également d'abréger le compte à rebours de fin de plongée de 3mn (ce temps de 3mn permet une éventuelle ré immersion en restant dans la même plongée).
> - **AUTO UP** : La simulation s'effectuant en temps fictif, qui s'écoule 10 fois, voire 100 fois plus rapidement que le temps réel, assurer une remontée à la bonne vitesse est pratiquement impossible. La touche **AUTO UP** permet de rejoindre le prochain palier à la vitesse de **12m/mn** jusqu'au premier palier, puis, **6m/mn** entre les différents paliers et la surface. Ce bouton permet de franchir le palier de confort de 3mn mais pas un palier obligatoire.
> - **RESET** : Retour a écran ***Avant la plongée***
> - **DÉTAIL DÉCO** : Enclenche le mode visualisation de la charge des compartiments. Ce mode est caché par défaut pour ne pas effrayer les plongeur N1 ou N2 qui n'ont pas connaitre les détails du modèle. Il permet, pendant la plongée, de faire apparaitre en temps réel le taux de charge des seize compartiments du modèle :
>
> <img src=img/img_3.png width="300px" />
>
> Ce mode est activé pour toute la durée de la plongée et ne peux pas être supprimé.

### Après la plongée

<img src=img/img_5.png width="600px" />

L'ordinateur reste actif après la plongée. les touches **START / STOP**, **FASTER**, **SLOWER**, **RESET** restent fonctionnelles. 

#### Affichage de l'ordinateur :

<img src=img/img_4.png width="300px" />

- **DESAT** : le temps avant désaturation complète.
- **INT SURF** : Le temps écoulé depuis la sortie de l'eau.
- **NO FLY** : Temps requis avant de pouvoir prendre l'avion.
- **Avertissement** : no fly, altitude interdite, palier omis.

#### Affichage des détails de calcul du modèle

Ce niveau de détail est destiné aux plongeurs expérimentés, préparant le N3, le N4, ...

<img src=img/img_10.png width="600px" />

> [!IMPORTANT]
>
> Cet affichage n'est disponible que si le mode **DÉTAIL DÉCO** a été enclenché durant la plongée. Vous pourrez alors choisir entre deux modes d'affichage avec le bouton **TIME / M-VALUE**.
>
> On peut voir la désaturation en temps accéléré des différents compartiments pendant l'intervalle de surface. 

##### Mode **TIME** :

<img src=img/img_9.png width="600px" />

Dans ce mode sous verrez pouvez observer les différentes **pressions** en fonction du **temps**.

- **En noir gras** : La pression absolue en bar.
- **En couleur** : Les tensions d'azote des différents compartiments en bar. Seuls les compartiments qui ont déclenché ou interrompu un palier sont représentés.

##### Mode **M-VALUE** :

<img src=img/img_8.png width="600px" />

Dans ce mode vous pouvez observer le plan **tension d'azote des différents compartiments** en fonction de la **pression absolue**.

- **En noir gras** : La droite des pressions ambiantes.
- **En noir pointillé** : Les droites des pressions plafond correspondantes aux profondeurs des paliers.
- **En couleur, trait plein** : L'évolution de la **tensions d'azote** dans différents compartiments en fonction de la pression absolue au cours de la plongée. Seuls les compartiments qui ont déclenché ou interrompu un palier sont représentés.
- **En couleur, trait pointillé** : Les droites de M-values de Bühlmann pour les compartiments qui ont déclenché ou interrompu un palier.

## Ressources et bibliographie

Ressources utilisées pour la conception de ce logiciel :

- Pour l'implémentation du modèle de Bühlmann :  [mf2-elements-de-calcul-pour-l-elaboration-d-un-logiciel-de-decompression.pdf](docs/mf2-elements-de-calcul-pour-l-elaboration-d-un-logiciel-de-decompression.pdf) 
- Pour comprendre les M-values :  [M-value.pdf](docs/M-value.pdf) 

## Code source

Le code source Python du simulateur est mis à disposition dans ce dépôt.

L'application utilise notamment les bibliothèques suivantes :

- Pygame pour l'interface graphique et les interactions ;
- Matplotlib pour les représentations graphiques ;
- NumPy pour les calculs numériques.

Les versions des dépendances sont indiquées dans le fichier `requirements.txt`.

### Exécution depuis les sources

Environnement utilisé pour le développement : **Python 3.10.11**.

Après avoir installé Python et récupéré le dépôt :

```
python -m pip install -r requirements.txt
python main.py
```

## Licence

Le code original du simulateur est distribué sous licence **PolyForm Noncommercial 1.0.0**.

Cette licence autorise notamment l'utilisation non commerciale, la modification et la redistribution du logiciel, sous réserve de respecter ses conditions.

Le texte intégral est disponible dans le fichier [`LICENSE`](LICENSE).

Le logiciel utilise également des composants tiers soumis à leurs propres licences, notamment Pygame sous GNU LGPL 2.1.

Les informations relatives aux bibliothèques, polices de caractères et illustrations utilisées sont regroupées dans [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md).

Les textes des licences tierces sont fournis dans le dossier `licenses/`.

## Auteur

Grégory COUTABLE

Projet développé à des fins pédagogiques et de découverte de la décompression en plongée.