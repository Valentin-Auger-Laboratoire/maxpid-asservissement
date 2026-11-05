"""Loi entrée-sortie du bras MaxPID : x(θ) et β(θ) (script écrit en 2026).

Géométrie (repère du bâti, O origine) :
  A = (a, 0)   pivot du bras 5 sur le bâti
  B = (0, b)   pivot du moteur (corps 2) sur le bâti
  C = A + c·(cos θ, sin θ)   extrémité du bras, liée à l'écrou 4
  x = BC       longueur variable, réglée par la vis (pas p, hélice à droite)

Fermeture géométrique  OA + AC + CB + BO = 0  →  x² = a² + b² + c² + 2c(a cos θ − b sin θ)
Système vis-écrou (ξ = −1) : x(θ) − x(θ0) = −p·β (β en tours), avec β0 = 0 pour θ0 = 0.
  →  β(θ) = (x(0) − x(θ)) / p,   x(0) = √((a + c)² + b²) = 170,51 mm

Usage : python loi_entree_sortie.py   (crée images/loi-entree-sortie.png si matplotlib est installé)
"""
import math
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

A, B, C = 69.5, 82.0, 80.0   # mm
P = 4.0                      # mm/tour

def x_de_theta(theta, somme_carres=A**2 + B**2 + C**2):
    return math.sqrt(somme_carres + 2 * C * (A * math.cos(theta) - B * math.sin(theta)))

X0 = x_de_theta(0.0)

def beta_exact(theta):
    """β en tours, avec β = 0 quand θ = 0 (OA et AC alignés)."""
    return (X0 - x_de_theta(theta)) / P

def beta_arrondi(theta):
    """Formule arrondie utilisée pour le tableau du TP : β = ¼[170 − √(18000 + 160(69,5 cos θ − 82 sin θ))]."""
    return 0.25 * (170 - math.sqrt(18000 + 160 * (69.5 * math.cos(theta) - 82 * math.sin(theta))))

def theta_de_beta(beta, loi):
    """Inverse par dichotomie (β croît avec θ sur [−0,5 ; 2,5] rad)."""
    lo, hi = -0.5, 2.5
    for _ in range(100):
        m = (lo + hi) / 2
        if loi(m) < beta:
            lo = m
        else:
            hi = m
    return math.degrees((lo + hi) / 2)

def regression(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    pente = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return pente, my - pente * mx

if __name__ == "__main__":
    print(f"a² + b² + c² = {A**2 + B**2 + C**2:.2f} (le tableau du TP utilise 18000)")
    print(f"x(0) = {X0:.2f} mm (le tableau du TP utilise 170)\n")
    betas = list(range(27))
    th_arr = [theta_de_beta(b, beta_arrondi) for b in betas]
    th_exa = [theta_de_beta(b, beta_exact) for b in betas]
    print(" β (tr) | θ formule arrondie (°) | θ exact (°) | écart (°)")
    for b, t1, t2 in zip(betas, th_arr, th_exa):
        print(f" {b:6d} | {t1:22.2f} | {t2:11.2f} | {t2 - t1:+.2f}")
    pente, ordo = regression(betas, th_arr)
    ecart = max(abs(t - (pente * b + ordo)) for b, t in zip(betas, th_arr))
    print(f"\nDroite des moindres carrés (formule arrondie) : θ = {pente:.4f}·β + {ordo:.4f}  "
          f"(mon tableur 2024 : 3,4121·β + 3,9088)")
    print(f"Écart maximal à la droite : {ecart:.2f}° → la loi n'est pas linéaire, "
          f"la pente locale varie de {th_arr[1]-th_arr[0]:.2f} à {th_arr[26]-th_arr[25]:.2f} °/tr")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        raise SystemExit("(matplotlib absent : pas de graphique)")
    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
    ax.plot(betas, th_exa, "-", color="#3b5b85", lw=2, label="loi exacte (θ(0) = 0)")
    ax.plot(betas, th_arr, "o", ms=4, color="#c8102e", label="formule arrondie (tableau du TP)")
    ax.plot(betas, [pente * b + ordo for b in betas], "--", color="#555", lw=1,
            label=f"droite θ = {pente:.3f}·β + {ordo:.2f}")
    ax.set_xlabel("β : tours de vis"); ax.set_ylabel("θ : angle du bras (°)")
    ax.set_title("MaxPID : loi entrée-sortie du bras"); ax.grid(alpha=.3); ax.legend()
    fig.tight_layout()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images", "loi-entree-sortie.png")
    fig.savefig(out); print("graphique :", os.path.normpath(out))
