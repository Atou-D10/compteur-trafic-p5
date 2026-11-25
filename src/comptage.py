"""Comptage des objets qui franchissent la ligne virtuelle."""


def centre(boite):
    """Renvoie le point (x, y) au milieu d'une boîte (x1, y1, x2, y2)."""
    x1, y1, x2, y2 = boite
    return (x1 + x2) / 2, (y1 + y2) / 2


def position_ligne(largeur_image, fraction):
    """Renvoie la position x (en pixels) de la ligne verticale."""
    return largeur_image * fraction


def cote(point, x_ligne):
    """Renvoie -1 si le point est à gauche de la ligne, +1 s'il est à droite."""
    x, _ = point
    return -1 if x < x_ligne else 1


class CompteurLigne:
    """Retient le côté de chaque objet, détecte les franchissements et compte."""

    def __init__(self, x_ligne):
        self.x_ligne = x_ligne
        self.dernier_cote = {}   # id de suivi -> -1 (gauche) ou +1 (droite)
        self.deja_comptes = set()   # id déjà comptés (anti double comptage)
        self.totaux = {"voiture": 0, "moto": 0, "bus": 0, "pieton": 0}
        self.passages = []   # liste de (temps_s, classe), pour le graphique

    def a_franchi(self, id_objet, boite):
        """Renvoie True si l'objet vient de changer de côté depuis l'image précédente."""
        nouveau = cote(centre(boite), self.x_ligne)
        ancien = self.dernier_cote.get(id_objet)
        self.dernier_cote[id_objet] = nouveau
        return ancien is not None and ancien != nouveau

    def mettre_a_jour(self, detection, temps_s):
        """À appeler pour chaque objet détecté. Renvoie True si on vient de le compter."""
        id_objet = detection["id"]
        if self.a_franchi(id_objet, detection["boite"]) and id_objet not in self.deja_comptes:
            self.deja_comptes.add(id_objet)
            self.totaux[detection["classe"]] += 1
            self.passages.append((temps_s, detection["classe"]))
            return True
        return False


    def compter_video(chemin_video=None):
        """Analyse toute la vidéo et renvoie le CompteurLigne rempli."""
        import cv2
        from src import config
        from src.detection import suivre_video

        chemin_video = chemin_video or config.VIDEO
        capture = cv2.VideoCapture(str(chemin_video))
        if not capture.isOpened():
            raise FileNotFoundError(f"Vidéo introuvable : {chemin_video}")
        fps = capture.get(cv2.CAP_PROP_FPS) or 30
        largeur = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        capture.release()

        compteur = CompteurLigne(position_ligne(largeur, config.LIGNE_X))
        for numero_image, _, detections in suivre_video(chemin_video):
            temps_s = numero_image / fps
            for d in detections:
                compteur.mettre_a_jour(d, temps_s)
        return compteur