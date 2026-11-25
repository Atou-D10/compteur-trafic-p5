"""Paramètres du compteur de trafic.

Tous les réglages sont ici : on les change à un seul endroit,
et les autres fichiers (detection, comptage, visualisation) les importent.
"""

from pathlib import Path

# --- Dossiers du projet -------------------------------------------------
RACINE = Path(__file__).resolve().parent.parent  # dossier compteur-trafic-p5
DOSSIER_VIDEOS = RACINE / "data" / "videos"
DOSSIER_SORTIES = RACINE / "outputs"

# Vidéo analysée : filmée par le groupe à Dakar (voir data/README.md)
VIDEO = DOSSIER_VIDEOS / "rue.mp4"

# --- Modèle YOLO --------------------------------------------------------
# yolo11n = YOLO11 version « nano » : la plus rapide, suffisante sur le GPU T4.
# Le fichier .pt est téléchargé automatiquement au premier lancement.
MODELE = "yolo11n.pt"

# Seuil de confiance : on ignore les détections dont YOLO est sûr à moins de 30 %.
CONFIANCE = 0.3

# --- Classes suivies (numéros du jeu de données COCO) -------------------
# YOLO connaît 80 classes ; on ne garde que ces 4.
CLASSES = {
    0: "pieton",  # person
    2: "voiture",  # car
    3: "moto",  # motorcycle
    5: "bus",  # bus
}

# --- Motards ----------------------------------------------------------
# YOLO voit le conducteur d'une moto comme un « piéton ». Si au moins 30 %
# de la boîte d'un piéton est dans la boîte d'une moto, c'est un motard :
# on l'enlève des piétons.
SEUIL_MOTARD = 0.3

# --- Suivi des objets ---------------------------------------------------
# ByteTrack donne un identifiant à chaque objet et le garde d'une image à l'autre.
TRACKER = "bytetrack.yaml"

# --- Ligne virtuelle (utilisée par la tâche 2) --------------------------
# Dans rue.mp4, les véhicules roulent de gauche à droite (et inversement) :
# la ligne est donc VERTICALE, et ils la franchissent en la traversant.
# Position horizontale de la ligne, en fraction de la largeur de l'image :
# 0.0 = tout à gauche, 0.5 = au milieu, 1.0 = tout à droite.
LIGNE_X = 0.5
