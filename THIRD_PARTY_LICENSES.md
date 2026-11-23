# Licences des composants tiers

Ce logiciel utilise plusieurs bibliothèques et ressources créées par des tiers. Chaque composant reste soumis à sa propre licence. Ces licences sont indépendantes de la licence applicable au code original du simulateur.

## 1. Bibliothèques Python

Les versions indiquées correspondent à l'environnement Python 3.10.11 utilisé pour le développement du logiciel.

| Bibliothèque    | Version | Licence                            |
| --------------- | ------: | ---------------------------------- |
| Pygame          |   2.6.1 | GNU LGPL 2.1                       |
| Matplotlib      |  3.10.9 | Python Software Foundation License |
| NumPy           |   2.2.6 | BSD 3-Clause                       |
| contourpy       |   1.3.2 | BSD 3-Clause                       |
| cycler          |  0.12.1 | BSD 3-Clause                       |
| fonttools       |  4.65.0 | MIT                                |
| kiwisolver      |   1.5.1 | BSD 3-Clause                       |
| packaging       |    26.3 | Apache 2.0 ou BSD 2-Clause         |
| Pillow          |  12.3.0 | HPND / MIT-CMU                     |
| pyparsing       |   3.3.3 | MIT                                |
| python-dateutil |   3.0.0 | Apache 2.0 ou BSD 3-Clause         |
| six             |  1.17.0 | MIT                                |
| tzdata          |  2026.6 | Apache 2.0                         |

Les textes de licence correspondants sont fournis dans le dossier `licenses/`, dans la mesure où ils sont distribués avec le projet.

### Cas particulier de Pygame

Pygame est distribué sous licence GNU LGPL version 2.1. Le texte de cette licence est fourni dans :

- `licenses/LGPL-2.1.txt`

Le code source de Pygame 2.6.1 est également mis à disposition afin de permettre son étude et sa modification.

Le projet utilise Pygame sans prétendre en être l'auteur. Toute modification éventuelle de Pygame reste soumise aux conditions de sa licence LGPL.

Pygame s'appuie lui-même sur d'autres bibliothèques, notamment SDL et certaines bibliothèques graphiques et audio. Les licences des composants tiers présents dans la distribution de Pygame doivent également être conservées avec les éléments correspondants.

## 2. Polices de caractères

Les polices suivantes sont utilisées dans le logiciel :

| Fichier                       | Licence                   |
| ----------------------------- | ------------------------- |
| `DSEG14Modern-BoldItalic.ttf` | DSEG License              |
| `DSEG7Classic-BoldItalic.ttf` | DSEG License              |
| `nervous_rex.ttf`             | Vic Fieger License        |
| `slkscr.ttf`                  | Kottke Silkscreen License |

Les textes de licence correspondants sont fournis dans le dossier `licenses/` :

- `DSEG-LICENSE.txt`
- `Vic Fieger License.txt`
- `Kottke Silkscreen License.txt`

## 3. Illustrations et sprites

Les sprites représentant le plongeur sont distribués sous licence **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

Cette licence autorise leur utilisation et leur modification, sous réserve de respecter les conditions d'attribution.

Référence de la licence : https://creativecommons.org/licenses/by/4.0/

L'attribution de l'auteur et la référence exacte de la ressource sont à préciser ici :

- Auteur : **Fellowship Of the Game**
- Source : https://opengameart.org/users/fellowship-of-the-game
- Modifications éventuelles : Aucunes modifications des dessins. Les sprites ont justes été réorganisés pour faciliter leur intégration dans le code.

L'animation graphique a été réalisée à partir d'une illustration vectorielle provenant de Vecteezy :

[Silhouette of coral reef with fish and divers – Vecteezy](https://www.vecteezy.com/vector-art/9102436-silhouette-of-coral-reef-with-fish-and-divers-on-blue-sea-background-underwater-vector-illustration).

## 4. Licence du logiciel

Les composants tiers cités dans ce document ne sont pas soumis à la licence du code original du simulateur.

Le code original du simulateur est distribué sous licence **PolyForm Noncommercial 1.0.0**, dont le texte est fourni dans le fichier `LICENSE` à la racine du dépôt.

En cas de différence entre les conditions de cette licence et celles d'une bibliothèque tierce, les conditions propres à cette bibliothèque s'appliquent à celle-ci.