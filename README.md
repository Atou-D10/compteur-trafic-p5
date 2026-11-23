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

En local (Python 3.10 ou plus) :

```bash
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

**Windows : si l'activation échoue** avec le message « l'exécution de scripts est désactivée sur ce système », c'est la politique d'exécution de PowerShell qui bloque le script. Autorisez-le pour la fenêtre en cours seulement, puis réactivez :

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.venv\Scripts\activate
```

Pour ne plus avoir à le refaire, remplacez `-Scope Process` par `-Scope CurrentUser`. Autre solution : utilisez l'invite de commandes (cmd) au lieu de PowerShell, avec `.venv\Scripts\activate.bat`.

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

| Membre | GitHub | Tâche |
|---|---|---|
| Fallou Mbaye | [@galassmyname](https://github.com/galassmyname) | 1 · Données, détection et suivi |
| Atou Diagne | [@Atou-D10](https://github.com/Atou-D10) | 2 · Comptage et graphique par minute |
| Maimouna Diallo | [@Mayra-99](https://github.com/Mayra-99) | 3 · Mesure, démo Gradio et livrables |

## Répartition des tâches

Les tâches se font l'une après l'autre.

---

### Tâche 1 · Données, détection et suivi — Fallou Mbaye


- [ ] Trouver ou filmer une vidéo de rue d'environ 3 minutes avec voitures, motos, bus et piétons (caméra fixe, de préférence en hauteur).
- [ ] Renseigner sa source et sa licence dans `data/README.md`.
- [ ] Compter à la main, sur **une minute** choisie, les voitures, motos, bus et piétons qui franchissent la ligne prévue. Noter le résultat dans `data/comptage_manuel.csv`. Cette minute ne sert pas à régler le système.
- [ ] `src/config.py` : modèle YOLO, seuil de confiance, classes COCO (piéton 0, voiture 2, moto 3, bus 5), position de la ligne.
- [ ] `src/detection.py` : charger YOLO et lancer le suivi (ByteTrack) sur la vidéo.
- [ ] Notebook : section « Détection et suivi » qui affiche quelques images avec les boîtes et les identifiants.

**Terminé quand :** sur Colab avec GPU, chaque véhicule ou piéton a une boîte et un identifiant qui reste à peu près stable pendant qu'il traverse l'image.

---

### Tâche 2 · Comptage et graphique — Atou Diagne


- [ ] `src/comptage.py` : détecter quand le centre d'un objet passe d'un côté de la ligne à l'autre. **Un identifiant n'est compté qu'une seule fois** (c'est le piège du sujet : éviter le double comptage).
- [ ] Garder, pour chaque passage, l'instant (en secondes) et la catégorie.
- [ ] `src/visualisation.py` : produire la vidéo annotée (ligne, boîtes, compteurs à l'écran) dans `outputs/`.
- [ ] `src/visualisation.py` : graphique du nombre de passages **par minute et par catégorie**.
- [ ] Notebook : sections « Comptage » et « Graphique par minute ».

**Terminé quand :** le notebook produit les totaux par catégorie, la vidéo annotée et le graphique sur la vidéo complète.

---

### Tâche 3 · Mesure, démo et livrables — Maimouna Diallo


- [ ] `src/evaluation.py` : comparer le comptage automatique au comptage manuel sur la même minute, et calculer l'erreur en % par catégorie : `|auto − manuel| / manuel × 100`.
- [ ] Remplir le tableau « Résultats » du README.
- [ ] Repérer et noter 2 ou 3 cas d'échec (occlusion, moto cachée par un bus, piétons groupés...).
- [ ] `app.py` : interface Gradio partageable. On dépose une vidéo, on obtient la vidéo annotée, les totaux et le graphique. Tester sur une **autre vidéo** que celle de la tâche 1 (le jury choisira l'entrée).
- [ ] `docs/schema_pipeline.png` : schéma du pipeline.
- [ ] `docs/fiche_technique.md` : choix d'outils justifiés, mesures, limites (une page).
- [ ] README complet : objectif, installation, utilisation, schéma, sources.

**Terminé quand :** la démo Gradio tourne sur une vidéo inconnue et tous les livrables sont dans le dépôt.

---

### Ensemble, à la fin

- [ ] Préparer la soutenance de 10 minutes dans `docs/soutenance/` : problème et utilisateur (1 min), schéma, démo en direct, mesures, limites.
- [ ] Répétition à trois, chronométrée.
- [ ] Bonus possible si le temps le permet : estimation de la vitesse.
