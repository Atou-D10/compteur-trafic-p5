# P5 · Compteur de trafic

Projet de l'atelier **IA Voix et Vidéo**. On compte automatiquement les **voitures, motos, bus et piétons** qui franchissent une ligne virtuelle dans une vidéo de rue, puis on compare avec un comptage manuel.

## Objectif

Mesurer le trafic d'une rue sans comptage manuel.

## Pipeline

```
Vidéo → détection YOLO → suivi ByteTrack → franchissement de la ligne → comptage par catégorie → graphique par minute
```

Schéma : `docs/schema_pipeline.png` (à ajouter).

## Structure du dépôt

| Dossier / fichier | Rôle |
|---|---|
| `src/config.py` | Paramètres : modèle, classes suivies, position de la ligne |
| `src/detection.py` | Détection et suivi des objets |
| `src/comptage.py` | Comptage au franchissement de la ligne |
| `src/visualisation.py` | Vidéo annotée et graphique par minute |
| `src/evaluation.py` | Comparaison avec le comptage manuel |
| `app.py` | Interface Gradio (démo) |
| `notebooks/compteur_trafic.ipynb` | Notebook Google Colab |
| `data/` | Vidéos (non versionnées) et comptage manuel |
| `docs/` | Schéma, fiche technique, soutenance |

## Installation (Google Colab)

1. Ouvrir `notebooks/compteur_trafic.ipynb` dans Colab.
2. Menu **Exécution → Modifier le type d'exécution → GPU T4**.
3. Exécuter les cellules dans l'ordre.

En local :

```bash
pip install -r requirements.txt
```

## Utilisation

```bash
python app.py
```

## Données

Voir `data/README.md` pour la source et la licence de chaque vidéo.

## Résultats

| Catégorie | Manuel (1 min) | Automatique | Erreur (%) |
|---|---|---|---|
| Voitures | | | |
| Motos | | | |
| Bus | | | |
| Piétons | | | |

## Limites

À compléter (cas d'échec observés).

## Équipe

- Atou
- May
- Fallou

Répartition des tâches : à compléter.
