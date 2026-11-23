# Simulateur d'ordinateur de plongée

**Auteur : Grégory COUTABLE**
**Copyright © 2026**

## Présentation

Ce projet est un simulateur pédagogique d'ordinateur de plongée. Il permet de visualiser et d'étudier le comportement d'un ordinateur de plongée, notamment à travers la simulation de profils d'immersion et le calcul de décompression basé sur le modèle de Bühlmann.

Il s'agit avant tout d'un outil de découverte, d'expérimentation et d'apprentissage.

## Avertissement important — Usage exclusivement pédagogique

**Ce logiciel ne doit en aucun cas être utilisé pour préparer, planifier ou conduire une plongée réelle.**

Les calculs et les simulations proposés ne constituent pas une aide à la décision pour la pratique de la plongée. Ils ne remplacent ni un ordinateur de plongée certifié, ni les procédures de sécurité, ni les recommandations d'un organisme de formation.

L'auteur décline toute responsabilité en cas d'utilisation de ce logiciel dans le cadre d'une plongée réelle.

## Exécutable

Un exécutable pour windows est disponible :

https://github.com/LANSIG/Simulateur-ordinateur-plongee/releases/tag/v3.4

Il suffit de le télécharger et de l'exécuter, il est 100% portable et ne nécessite aucune installation. Il a été créé avec `pyinstaller` et peut injustement nécessiter un contrôle supplémentaire de votre anti-virus.

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

## Documentation

La documentation complémentaire du logiciel est disponible dans les fichiers de documentation du dépôt.

## Auteur

Grégory COUTABLE

Projet développé à des fins pédagogiques et de découverte de la décompression en plongée.