# Simulation d'un ordinateur de plongée

***Version 3.4***

<img src=img/img_11.png width="600px" />

## Usage

Ce programme a pour but de permettre la visualisation, hors de l'eau du comportement d'un ordinateur de plongée, avant, pendant, et après l'immersion. Il applique strictement l'algorithme de **Bühlmann** (1924-1994) avec ses seize compartiments. Ce programme est a utiliser dans le cadre de l'enseignement de la plongée. Il ne doit en aucun cas servir a planifier la procédure de décompression d'une plongée réelle, pour cela, vous devez impérativement utiliser un ordinateur de plongée ou des tables qui ont été validés par les autorités compétentes.

## Interface graphique

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

- Pour l'implémentation du modèle de Bühlmann : ` [mf2-elements-de-calcul-pour-l-elaboration-d-un-logiciel-de-decompression.pdf](docs\mf2-elements-de-calcul-pour-l-elaboration-d-un-logiciel-de-decompression.pdf) `
- Pour comprendre les M-values : ` [M-value.pdf](docs\M-value.pdf) `

## Avertissement – Usage exclusivement pédagogique

Ce logiciel est un simulateur informatique destiné exclusivement à l'enseignement et à la compréhension des principes de fonctionnement d'un ordinateur de plongée.

**IL NE DOIT EN AUCUN CAS ÊTRE UTILISÉ POUR PRÉPARER, PLANIFIER, CONDUIRE OU CONTRÔLER UNE PLONGÉE RÉELLE.**

Ce logiciel ne constitue pas un ordinateur de plongée certifié ni un outil de planification de décompression.

Les résultats fournis sont purement indicatifs et ne présentent aucune garantie d'exactitude, de fiabilité ou de sécurité dans le cadre d'une utilisation opérationnelle.

Ils ne doivent jamais servir à déterminer un profil de plongée, des durées d'immersion, des profondeurs, des paliers de décompression ou toute autre décision relative à la sécurité d'une plongée.

L'auteur décline toute responsabilité concernant les conséquences d'une utilisation détournée du logiciel, notamment dans le cadre d'une plongée réelle, dans les limites autorisées par la législation applicable.

**L'utilisation de ce logiciel relève de la seule responsabilité de son utilisateur.**

## Auteur et propriété intellectuelle

Ce logiciel a été conçu et développé par **Grégory COUTABLE**.

***© Copyright Grégory COUTABLE 2026***. Tous droits réservés, sous réserve des droits attachés aux ressources tierces.

Ce logiciel est distribué sous licence **PolyForm Noncommercial 1.0.0**.

Vous êtes autorisé à télécharger, utiliser, étudier, modifier et redistribuer ce logiciel, y compris dans des versions modifiées, à des fins non commerciales, sous réserve du respect des conditions de cette licence.

Toute utilisation commerciale nécessite l'autorisation préalable et écrite de l'auteur.

Le texte intégral de la licence est disponible dans le fichier `LICENSE` à la racine du dépôt.

La licence applicable au code source et aux éléments originaux du logiciel est précisée dans le fichier `LICENSE` à la racine du dépôt GitHub.

#### Avertissement – Usage exclusivement pédagogique

Ce logiciel est un simulateur informatique destiné exclusivement à l'enseignement et à la compréhension des principes de fonctionnement d'un ordinateur de plongée.

**IL NE DOIT EN AUCUN CAS ÊTRE UTILISÉ POUR PRÉPARER, PLANIFIER, CONDUIRE OU CONTRÔLER UNE PLONGÉE RÉELLE.**

Ce logiciel ne constitue pas un ordinateur de plongée certifié ni un outil de planification de décompression.

Les résultats fournis sont purement indicatifs et ne présentent aucune garantie d'exactitude, de fiabilité ou de sécurité dans le cadre d'une utilisation opérationnelle.

Ils ne doivent jamais servir à déterminer un profil de plongée, des durées d'immersion, des profondeurs, des paliers de décompression ou toute autre décision relative à la sécurité d'une plongée.

L'auteur décline toute responsabilité concernant les conséquences d'une utilisation détournée du logiciel, notamment dans le cadre d'une plongée réelle, dans les limites autorisées par la législation applicable.

**L'utilisation de ce logiciel relève de la seule responsabilité de son utilisateur.**

#### Crédit image

L'animation graphique a été réalisée à partir d'une illustration vectorielle provenant de Vecteezy :

[Silhouette of coral reef with fish and divers – Vecteezy](https://www.vecteezy.com/vector-art/9102436-silhouette-of-coral-reef-with-fish-and-divers-on-blue-sea-background-underwater-vector-illustration).

Cette illustration reste soumise à sa licence d'origine et aux conditions d'utilisation de son auteur.







