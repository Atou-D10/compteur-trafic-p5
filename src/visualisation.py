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