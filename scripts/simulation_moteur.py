"""Re-simulation du moteur à courant continu avec les valeurs de la fiche (script écrit en 2026).

Modèle :
  U = R·i + L·di/dt + e        e = Ke·Ω
  J·dΩ/dt = Kt·i − f·Ω − Cr

Valeurs de la fiche du moteur (voir docs/valeurs.md) ; l'inertie J n'y figure pas : elle est SUPPOSÉE.
Le frottement visqueux f est calé pour retrouver le courant à vide de la fiche (20 mA).
Usage : python simulation_moteur.py   (crée images/simulation-moteur.png si matplotlib est installé)
"""
import math
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

U = 12.0                                  # V, tension nominale
R = 9.5                                   # Ω, résistance de l'induit (fiche)
L = 0.82e-3                               # H, inductance de l'induit (fiche)
KT = 9.62e-3                              # N·m/A, constante de couple (fiche)
KV = 953.0                                # tr/min/V, constante de vitesse (fiche)
KE = 60.0 / (2 * math.pi * KV)            # V·s/rad, déduite de Kv
I0 = 0.020                                # A, courant à vide (fiche)
J = 1.0e-6                                # kg·m², SUPPOSÉE (ordre de grandeur d'un petit moteur)
CR = 0.0                                  # N·m, à vide

# frottement visqueux calé sur I0 en régime permanent : Kt·I0 = f·Ω∞ et U = R·I0 + Ke·Ω∞
OMEGA_INF = (U - R * I0) / KE
F = KT * I0 / OMEGA_INF

def simuler(t_fin=0.6, dt=2e-6):
    def deriv(i, w):
        return (U - R * i - KE * w) / L, (KT * i - F * w - CR) / J
    t, i, w = 0.0, 0.0, 0.0
    ts, Is, Ws = [0.0], [0.0], [0.0]
    pas = int(t_fin / dt)
    for k in range(pas):                   # Runge-Kutta 4
        a1, b1 = deriv(i, w)
        a2, b2 = deriv(i + a1 * dt / 2, w + b1 * dt / 2)
        a3, b3 = deriv(i + a2 * dt / 2, w + b2 * dt / 2)
        a4, b4 = deriv(i + a3 * dt, w + b3 * dt)
        i += dt * (a1 + 2 * a2 + 2 * a3 + a4) / 6
        w += dt * (b1 + 2 * b2 + 2 * b3 + b4) / 6
        t += dt
        if k % 50 == 0:
            ts.append(t); Is.append(i); Ws.append(w)
    return ts, Is, Ws

if __name__ == "__main__":
    tau_e = L / R
    tau_m = J * R / (KE * KT + F * R)
    print(f"Ke = {KE:.5f} V·s/rad   Kt = {KT:.5f} N·m/A   (cohérents à {abs(KE-KT)/KT*100:.1f} %)")
    print(f"Courant de démarrage U/R = {U/R:.3f} A (fiche : 1,26 A) ; couple de démarrage = {KT*U/R*1e3:.2f} mN·m (fiche : 11,5)")
    print(f"Frottement calé f = {F:.3e} N·m·s/rad")
    print(f"Vitesse à vide du modèle = {OMEGA_INF:.0f} rad/s = {OMEGA_INF*60/(2*math.pi):.0f} tr/min (fiche : 8 700 tr/min)")
    print(f"Constantes de temps : électrique τe = L/R = {tau_e*1e6:.0f} µs, mécanique τm ≈ {tau_m*1e3:.0f} ms (avec J supposée)")
    ts, Is, Ws = simuler()
    k63 = next(k for k, w in enumerate(Ws) if w >= 0.632 * Ws[-1])
    print(f"Vitesse à 63 % de la valeur finale atteinte à t = {ts[k63]*1e3:.0f} ms")
    print(f"Courant max = {max(Is):.3f} A, courant final = {Is[-1]*1e3:.1f} mA")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        raise SystemExit("(matplotlib absent : pas de graphique)")
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.8), dpi=110)
    a1.plot([t * 1e3 for t in ts], [w * 60 / (2 * math.pi) for w in Ws], color="#3b5b85", lw=2)
    a1.axvline(tau_m * 1e3, ls="--", color="#555", lw=1); a1.text(tau_m * 1e3 + 8, 1000, "τm", color="#555")
    a1.set_xlabel("t (ms)"); a1.set_ylabel("vitesse (tr/min)"); a1.set_title("Vitesse : montée exponentielle")
    a2.plot([t * 1e3 for t in ts], Is, color="#c8102e", lw=2)
    a2.set_xlabel("t (ms)"); a2.set_ylabel("courant (A)"); a2.set_title("Courant : pic au démarrage puis I0")
    for a in (a1, a2): a.grid(alpha=.3)
    fig.suptitle(f"Moteur CC, valeurs de la fiche, U = 12 V à vide (J = {J:.0e} kg·m² supposée)", fontsize=10)
    fig.tight_layout()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images", "simulation-moteur.png")
    fig.savefig(out); print("graphique :", os.path.normpath(out))
