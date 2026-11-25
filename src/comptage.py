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