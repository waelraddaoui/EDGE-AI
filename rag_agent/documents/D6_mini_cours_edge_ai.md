# Document D6 : Mini-Cours Synthétique sur l'IA Embarquée (Edge AI)

## 1. Définition et Enjeux du Edge AI
L'**Edge AI** consiste à exécuter des algorithmes d'apprentissage automatique directement au plus près des capteurs (sur microcontrôleurs ou nano-ordinateurs type Raspberry Pi), sans dépendre d'une connexion réseau permanente vers le Cloud.

### Avantages Industriels Clés :
- **Ultra-Faible Latence** : Traitement temps réel en moins de quelques millisecondes.
- **Confidentialité et Sécurité** : Les données vibratoires brutes restent locales et ne sont pas transférées sur Internet.
- **Autonomie Réseau** : Continuité de fonctionnement même en cas de coupure de réseau.
- **Réduction des Coûts de Bande Passante** : Envoi uniquement des alertes et résumés de santé matérielle.

## 2. Fenêtrage Temporel et Prétraitement Embarqué
Les signaux haute fréquence (ex: 12 kHz) sont découpés en fenêtres glissantes (ex: 1024 points avec 50% de chevauchement). Sur chaque fenêtre, une extraction de caractéristiques temporelles et fréquentielles réduites (16 valeurs) permet de compacter l'information avant transmission au modèle d'IA.
