"""Comptage des objets qui franchissent la ligne virtuelle."""


def centre(boite):
    """Renvoie le point (x, y) au milieu d'une boîte (x1, y1, x2, y2)."""
    x1, y1, x2, y2 = boite
    return (x1 + x2) / 2, (y1 + y2) / 2