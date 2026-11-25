"""Vidéo annotée et graphique des passages par minute."""

from pathlib import Path

import matplotlib.pyplot as plt

CATEGORIES = ["voiture", "moto", "bus", "pieton"]


def passages_par_minute(passages):
    """Range les passages (temps_s, classe) par minute.

    Renvoie un dictionnaire : classe -> liste du nombre de passages par minute.
    """
    if not passages:
        return {c: [] for c in CATEGORIES}
    nb_minutes = int(max(t for t, _ in passages) // 60) + 1
    comptes = {c: [0] * nb_minutes for c in CATEGORIES}
    for t, classe in passages:
        comptes[classe][int(t // 60)] += 1
    return comptes


def graphique_par_minute(passages, chemin_sortie="outputs/graphique_par_minute.png"):
    """Trace un graphique en barres des passages par minute et par catégorie."""
    comptes = passages_par_minute(passages)
    nb_minutes = len(comptes["voiture"])
    largeur = 0.2  # largeur d'une barre ; 4 barres côte à côte par minute

    fig, ax = plt.subplots(figsize=(9, 4))
    for i, classe in enumerate(CATEGORIES):
        positions = [m + (i - 1.5) * largeur for m in range(nb_minutes)]
        ax.bar(positions, comptes[classe], width=largeur, label=classe)

    ax.set_xticks(range(nb_minutes))
    ax.set_xticklabels([f"{m}:00 - {m + 1}:00" for m in range(nb_minutes)])
    ax.set_xlabel("Minute de la vidéo")
    ax.set_ylabel("Nombre de passages")
    ax.set_title("Passages sur la ligne, par minute et par catégorie")
    ax.legend()
    fig.tight_layout()

    Path(chemin_sortie).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(chemin_sortie)
    plt.close(fig)
    return comptes


def video_comptage(chemin_video=None, chemin_sortie="outputs/comptage.mp4"):
    """Crée la vidéo annotée (ligne, boîtes, compteurs) et renvoie le compteur rempli."""
    import cv2
    from src import config
    from src.comptage import CompteurLigne, position_ligne
    from src.detection import dessiner, suivre_video

    chemin_video = chemin_video or config.VIDEO
    capture = cv2.VideoCapture(str(chemin_video))
    if not capture.isOpened():
        raise FileNotFoundError(f"Vidéo introuvable : {chemin_video}")
    fps = capture.get(cv2.CAP_PROP_FPS) or 30
    largeur = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    hauteur = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    capture.release()

    x_ligne = int(position_ligne(largeur, config.LIGNE_X))
    compteur = CompteurLigne(x_ligne)

    Path(chemin_sortie).parent.mkdir(parents=True, exist_ok=True)
    ecriture = cv2.VideoWriter(
        str(chemin_sortie), cv2.VideoWriter_fourcc(*"mp4v"), fps, (largeur, hauteur)
    )

    for numero_image, image, detections in suivre_video(chemin_video):
        for d in detections:
            compteur.mettre_a_jour(d, numero_image / fps)

        dessiner(image, detections)  # boîtes et identifiants (code de Fallou)
        cv2.line(image, (x_ligne, 0), (x_ligne, hauteur), (0, 0, 255), 3)  # ligne rouge

        # Compteurs en haut à gauche, sur un fond noir pour être lisibles
        cv2.rectangle(image, (10, 10), (260, 150), (0, 0, 0), -1)
        for i, classe in enumerate(CATEGORIES):
            texte = f"{classe} : {compteur.totaux[classe]}"
            cv2.putText(image, texte, (20, 45 + i * 32),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        ecriture.write(image)
        if numero_image % 300 == 0:
            print(f"image {numero_image} : {compteur.totaux}")

    ecriture.release()
    print("Vidéo annotée :", chemin_sortie)
    return compteur