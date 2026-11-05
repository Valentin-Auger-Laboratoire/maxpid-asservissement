# Valeurs et équations / Values and equations

## 1. Cinématique du bras

| Grandeur | Valeur | Rôle |
|---|---|---|
| a = OA | 69,5 mm | O : origine du bâti, A : pivot du bras 5 sur le bâti (sur x₁) |
| b = OB | 82 mm | B : pivot du corps moteur 2 sur le bâti (sur y₁) |
| c = AC | 80 mm | C : liaison bras 5 / écrou 4 |
| x = BC | variable | longueur réglée par la vis |
| p | 4 mm/tour | pas de la vis (hélice à droite, ξ = −1) |
| θ | 0 à ≈ 92° | angle du bras 5 par rapport à x₁ |
| β | 0 à 26 tours | rotation de la vis 3 par rapport au corps 2 |

Équations :
- Fermeture géométrique : **OA + AC + CB + BO = 0**
- Projection sur x₁ : `a + c·cos θ − x·cos α = 0` et sur y₁ : `c·sin θ + x·sin α − b = 0` (α : angle de BC par rapport à x₁, compté vers le bas)
- **x(θ) = √(a² + b² + c² + 2c(a·cos θ − b·sin θ))**, avec a² + b² + c² = **17 954,25 mm²**
- Vis-écrou : `x(θ) − x(θ₀) = −p·β` (β en tours), soit `dx/dt = −(p/2π)·dβ/dt` (β en rad)
- Avec β = 0 pour θ = 0 : **β(θ) = (x(0) − x(θ)) / p**, avec **x(0) = √((a + c)² + b²) = 170,51 mm**
- Formule arrondie du sujet : β = ¼·[170 − √(18000 + 160(69,5·cos θ − 82·sin θ))]. Elle donne θ = 0,95° pour β = 0, puis un écart de 0,56 à 0,95° avec la loi exacte.
- Loi presque linéaire : droite des moindres carrés θ ≈ 3,412·β + 7,32 (°), écart maximal 6,4°. La pente locale passe de 5,6 °/tr (β ≈ 0) à 2,9 °/tr (β ≈ 26).

## 2. Moteur à courant continu

### Fiche du moteur (utilisée en 2024)

| Grandeur | Valeur |
|---|---|
| Tension nominale U | 12 V |
| Vitesse à vide | 8 700 tr/min |
| Courant à vide I₀ | 20 mA |
| Couple de démarrage | 11,5 mN·m |
| Courant de démarrage | 1,26 A |
| Résistance de l'induit R | 9,5 Ω |
| Constante de vitesse Kv | 953 tr/min/V, donc **Ke = 60 / (2π·953) = 0,01002 V·s/rad** |
| Constante de couple Kt | **9,62 mN·m/A = 0,00962 N·m/A** |
| Inductance de l'induit L | 0,82 mH |

### Valeurs ajoutées en 2026 (hypothèses)

| Grandeur | Valeur | Origine |
|---|---|---|
| Inertie J (rotor seul) | **1,0·10⁻⁶ kg·m²**, **SUPPOSÉE** | absente de la fiche ; ordre de grandeur d'un petit moteur |
| Frottement visqueux f | 1,63·10⁻⁷ N·m·s/rad | calé pour retrouver I₀ = 20 mA en régime permanent |
| Couple résistant Cr | 0 | essai à vide |

### Équations
- `U = R·i + L·di/dt + e`, avec `e = Ke·Ω`
- `J·dΩ/dt = Kt·i − f·Ω − Cr`
- Constante de temps électrique : `τe = L/R ≈ 86 µs`
- Constante de temps mécanique : `τm = J·R / (Ke·Kt + f·R) ≈ 97 ms` (avec la J supposée)
- Vitesse à vide du modèle : `Ω∞ = (U − R·I₀)/Ke ≈ 1 179 rad/s ≈ 11 255 tr/min`, alors que la fiche annonce 8 700 tr/min (voir la relecture)

### Ce que montrait la simulation Simscape de 2024 (lu sur les captures)
- Tension : 12 V constante.
- Courant : environ 0,63 A, presque constant sur 10 s.
- Vitesse : rampe droite de 0 à environ 8,3 rad/s en 10 s.
- Ce résultat est incompatible avec la fiche : il faudrait 1,26 A au démarrage, puis une montée exponentielle en environ 0,1 s.

### Mesures du banc (synthèse de 2024)
Résistance de l'induit mesurée entre 1,99 et 2,94 Ω, selon la méthode. C'est loin des 9,5 Ω de la fiche.
