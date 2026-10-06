# Document D13 : Norme Industrielle ISO 10816-3 et Procédures de Sécurité LOTO

## Classification Vibratoire selon la Norme ISO 10816-3
La norme internationale **ISO 10816-3** (remplacée par ISO 20816-3) définit les seuils d'évaluation de la sévérité vibratoire pour les machines industrielles en fonction de la vitesse efficace globale ($RMS$ en $\text{mm/s}$ dans la bande 10 Hz – 1000 Hz) et de la puissance de la machine.

Pour les moteurs électriques et pompes industrielles de classe moyenne (15 kW à 300 kW, support rigide) :

| Zone ISO | Vitesse RMS (mm/s) | État Machine | Action de Maintenance Requise |
| :---: | :---: | :---: | :--- |
| **Zone A** | $V_{RMS} < 1.4\,\text{mm/s}$ | **État Excellent (Neuf)** | Fonctionnement sans restriction, état nominal. |
| **Zone B** | $1.4 \le V_{RMS} < 2.8\,\text{mm/s}$ | **État Acceptable** | Fonctionnement continu sans restriction à long terme. |
| **Zone C** | $2.8 \le V_{RMS} < 4.5\,\text{mm/s}$ | **État Insatisfaisant (Alerte)** | Fonctionnement limité dans le temps. Planifier une intervention sous 2 à 4 semaines. |
| **Zone D** | $V_{RMS} \ge 4.5\,\text{mm/s}$ | **État Inacceptable (Danger)** | Risque de casse catastrophique immédiate. **Arrêt d'urgence obligatoire**. |

## Procédure de Consignation et Sécurité Industrielle (LOTO - Lockout/Tagout)
Avant toute intervention mécanique ou démontage de roulement :

1. **Information** : Prévenir les opérateurs et le chef de quart de l'arrêt de la ligne.
2. **Séparation Électrique** : Ouvrir le disjoncteur principal du variateur de vitesse / moteur.
3. **Condamnation (Lockout)** : Poser un cadenas de sécurité individuel sur le sectionneur avec étiquette d'avertissement (Tagout).
4. **Dissipation des Énergies Résiduelles** : Vérifier l'arrêt complet de l'inertie de rotation et purger les circuits sous pression/condensateurs.
5. **Vérification d'Absence de Tension (VAT)** : Mesurer au multimètre/testeur VAT avant tout contact mécanique.

## Procédure de Montage et Remplacement de Roulement
- **Chauffage par Induction** : Le roulement neuf SKF doit être chauffé de manière homogène à **110°C** (jamais au chalumeau pour préserver les traitements thermiques de l'acier chromé 100Cr6).
- **Emmanchement** : Poser la bague intérieure sur la portée d'arbre sans choc mécanique avec douille de montage appropriée.
- **Lubrification** : Appliquer la graisse recommandée (polyurée ou lithium complexe) en remplissant 30% à 50% de l'espace libre du palier.
- **Alignement Laser** : Vérifier le désalignement angulaire (< 0.05 mm/100 mm) et parallèle (< 0.05 mm) entre moteur et charge.
