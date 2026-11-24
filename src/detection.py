"""Détection et suivi des objets avec YOLO + ByteTrack.

Pour chaque image de la vidéo :
  1. YOLO trouve les objets (boîte + classe + confiance) ;
  2. ByteTrack relie les boîtes d'une image à l'autre et donne à chaque
     objet un identifiant (id) qui reste le même tant qu'il est visible.

Ce fichier fournit la fonction `suivre_video`, utilisée par la tâche 2
(comptage), et un petit programme de test qui produit une vidéo annotée.

Lancer le test (depuis le dossier compteur-trafic-p5) :
    python -m src.detection
"""

import cv2
from ultralytics import YOLO

from src import config


def charger_modele(nom=config.MODELE):
    """Charge le modèle YOLO (téléchargé automatiquement la 1re fois)."""
    return YOLO(nom)


def part_dans(petite, grande):
    """Part (de 0 à 1) de la boîte `petite` qui se trouve dans la boîte `grande`."""
    x1 = max(petite[0], grande[0])
    y1 = max(petite[1], grande[1])
    x2 = min(petite[2], grande[2])
    y2 = min(petite[3], grande[3])
    intersection = max(0, x2 - x1) * max(0, y2 - y1)
    aire = (petite[2] - petite[0]) * (petite[3] - petite[1])
    return intersection / aire if aire > 0 else 0


def enlever_motards(detections, seuil=config.SEUIL_MOTARD):
    """Enlève les « piétons » qui sont en fait assis sur une moto."""
    motos = [d["boite"] for d in detections if d["classe"] == "moto"]
    gardees = []
    for d in detections:
        if d["classe"] == "pieton" and any(
            part_dans(d["boite"], m) >= seuil for m in motos
        ):
            continue  # c'est un motard : on ne le garde pas
        gardees.append(d)
    return gardees


def suivre_video(chemin_video=config.VIDEO, modele=None):
    """Analyse la vidéo image par image.

    C'est un générateur : à chaque tour de boucle il renvoie
        (numero_image, image, detections)
    où `detections` est une liste de dictionnaires :
        {"id": 7, "classe": "voiture", "confiance": 0.82,
         "boite": (x1, y1, x2, y2)}
    Les coordonnées sont en pixels (x vers la droite, y vers le bas).
    """
    if modele is None:
        modele = charger_modele()

    resultats = modele.track(
        source=str(chemin_video),
        stream=True,  # une image à la fois : pas de saturation mémoire
        persist=True,  # garde les identifiants d'une image à l'autre
        tracker=config.TRACKER,
        classes=list(config.CLASSES),  # seulement piéton, voiture, moto, bus
        conf=config.CONFIANCE,
        verbose=False,
    )

    for numero_image, r in enumerate(resultats):
        detections = []
        boites = r.boxes
        # Au tout début, ByteTrack n'a parfois pas encore donné d'id : on saute.
        if boites is not None and boites.id is not None:
            for xyxy, ident, cls, conf in zip(
                boites.xyxy.tolist(),
                boites.id.int().tolist(),
                boites.cls.int().tolist(),
                boites.conf.tolist(),
            ):
                detections.append(
                    {
                        "id": ident,
                        "classe": config.CLASSES[cls],
                        "confiance": round(conf, 2),
                        "boite": tuple(int(v) for v in xyxy),
                    }
                )
        detections = enlever_motards(detections)
        yield numero_image, r.orig_img, detections


def dessiner(image, detections):
    """Dessine les boîtes et les étiquettes « id classe » sur l'image."""
    for d in detections:
        x1, y1, x2, y2 = d["boite"]
        couleur = (0, 200, 0)
        cv2.rectangle(image, (x1, y1), (x2, y2), couleur, 2)
        texte = f'#{d["id"]} {d["classe"]}'
        cv2.putText(
            image,
            texte,
            (x1, max(y1 - 8, 15)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            couleur,
            2,
        )
    return image


def video_annotee(
    chemin_video=config.VIDEO, chemin_sortie=config.DOSSIER_SORTIES / "detection.mp4"
):
    """Crée une vidéo avec les boîtes et les identifiants, pour vérifier le suivi.

    Renvoie un résumé : nombre d'objets différents (ids) vus par classe.
    """
    capture = cv2.VideoCapture(str(chemin_video))
    if not capture.isOpened():
        raise FileNotFoundError(f"Vidéo introuvable : {chemin_video}")
    fps = capture.get(cv2.CAP_PROP_FPS) or 30
    largeur = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    hauteur = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    capture.release()

    chemin_sortie.parent.mkdir(parents=True, exist_ok=True)
    ecriture = cv2.VideoWriter(
        str(chemin_sortie), cv2.VideoWriter_fourcc(*"mp4v"), fps, (largeur, hauteur)
    )

    ids_par_classe = {nom: set() for nom in config.CLASSES.values()}
    for numero_image, image, detections in suivre_video(chemin_video):
        for d in detections:
            ids_par_classe[d["classe"]].add(d["id"])
        ecriture.write(dessiner(image, detections))
        if numero_image % 100 == 0:
            print(f"image {numero_image} : {len(detections)} objets")
    ecriture.release()

    resume = {nom: len(ids) for nom, ids in ids_par_classe.items()}
    print("Vidéo annotée :", chemin_sortie)
    print("Objets différents vus (ids) :", resume)
    return resume


if __name__ == "__main__":
    video_annotee()
