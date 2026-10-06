# Document D2 : Fiche Technique Industrielle des Roulements SKF 6205-2RS

## 1. Caractéristiques Géométriques du Roulement
- **Modèle** : SKF 6205-2RS JEM (Roulement rigide à billes à un rang)
- **Diamètre intérieur (\(d\))** : 25 mm
- **Diamètre extérieur (\(D\))** : 52 mm
- **Diamètre moyen (\(D_m\))** : 38.5 mm
- **Diamètre des billes (\(d_b\))** : 7.94 mm (0.3126 in)
- **Nombre de billes (\(N\))** : 9 billes
- **Angle de contact (\(\theta\))** : 0°

## 2. Fréquences Cinématiques de Défaillance (pour une vitesse N = 1772 RPM, \(f_r = 29.53\) Hz)
Les fréquences caractéristiques de passage des défauts se calculent via les formules cinématiques :

1. **BPFI (Ball Pass Frequency Inner Race)** :
   \[
   BPFI = \frac{N}{2} \cdot f_r \cdot \left(1 + \frac{d_b}{D_m} \cos\theta\right) \approx 162.19 \text{ Hz} \quad (5.43 \times f_r)
   \]
2. **BPFO (Ball Pass Frequency Outer Race)** :
   \[
   BPFO = \frac{N}{2} \cdot f_r \cdot \left(1 - \frac{d_b}{D_m} \cos\theta\right) \approx 103.58 \text{ Hz} \quad (3.57 \times f_r)
   \]
3. **BSF (Ball Spin Frequency)** :
   \[
   BSF = \frac{D_m}{2 d_b} \cdot f_r \cdot \left(1 - \left(\frac{d_b}{D_m}\right)^2 \cos^2\theta\right) \approx 67.44 \text{ Hz} \quad (2.32 \times f_r)
   \]
4. **FTF (Fundamental Train Frequency - Cage)** :
   \[
   FTF = \frac{f_r}{2} \cdot \left(1 - \frac{d_b}{D_m} \cos\theta\right) \approx 11.51 \text{ Hz} \quad (0.39 \times f_r)
   \]

## 3. Modes de Défaillance Principaux
- **Écaillage (Spalling)** : Dégradation de surface causée par la fatigue de contact sous charge cyclique.
- **Micro-grippage (Galling)** : Manque de lubrification provoquant un transfert de matière.
- **Empreinte d'impact** : Choc mécanique direct déformant la piste de roulement.
