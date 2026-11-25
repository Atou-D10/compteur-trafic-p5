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
    """Retient le côté de chaque objet et détecte quand il franchit la ligne."""

    def __init__(self, x_ligne):
        self.x_ligne = x_ligne
        self.dernier_cote = {}   # id de suivi -> -1 (gauche) ou +1 (droite)

    def a_franchi(self, id_objet, boite):
        """Renvoie True si l'objet vient de changer de côté depuis l'image précédente."""
        nouveau = cote(centre(boite), self.x_ligne)
        ancien = self.dernier_cote.get(id_objet)   # None si on voit l'objet pour la première fois
        self.dernier_cote[id_objet] = nouveau
        return ancien is not None and ancien != nouveau