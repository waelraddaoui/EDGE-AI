# Document D11 : Optimisation et Déploiement sur Edge AI

## 1. Définition et Intérêt du Edge Computing
L'Edge Computing, ou informatique à la périphérie, consiste à traiter les données au plus près de l'endroit où elles sont générées (par exemple, directement sur le capteur de la machine), plutôt que de les envoyer vers un Data Center (Cloud).
- **Faible Latence** : La réponse est immédiate. Indispensable lorsqu'il faut stopper en urgence une machine dangereuse.
- **Bande Passante (Bandwidth)** : Transmettre 20 000 points de mesure vibratoire par seconde vers le cloud sature la bande passante. Traiter en local permet de n'envoyer qu'un octet (ex: "Etat = Sain").
- **Sécurité et Confidentialité** : Les données sensibles ne quittent pas l'usine.
- **Résilience** : Le système fonctionne même si la connexion internet de l'usine est coupée.

## 2. Défis de l'Edge AI
Les microcontrôleurs (Arduino) ou les nano-ordinateurs (Raspberry Pi) possèdent des ressources extrêmement limitées par rapport à un serveur :
- RAM limitée (souvent quelques Mo ou Go).
- Puissance de calcul CPU/GPU restreinte.
- Contraintes de consommation électrique (fonctionnement sur batterie).

## 3. Techniques d'Optimisation des Modèles
Pour faire tourner un gros réseau de neurones sur un petit appareil, les ingénieurs utilisent des techniques d'optimisation radicales :
### A. La Quantification (Quantization)
Les modèles Deep Learning sont généralement entraînés avec une précision en virgule flottante de 32 bits (Float32). La quantification consiste à réduire cette précision, par exemple en nombres entiers de 8 bits (Int8).
- **Avantage** : Le modèle prend 4 fois moins de place en mémoire, et l'inférence est beaucoup plus rapide.
- **Inconvénient** : Une très légère perte de précision algorithmique (accuracy).

### B. L'Élagage (Pruning)
Un réseau de neurones est constitué de milliers de connexions (poids). Certaines connexions ont des valeurs très proches de zéro et n'influencent pas vraiment la prédiction. L'élagage supprime ces connexions "inutiles".
- **Résultat** : Un réseau "clairsemé" (Sparse Network) beaucoup plus léger et rapide à exécuter.

### C. La Distillation des Connaissances (Knowledge Distillation)
On utilise un énorme modèle (le "Professeur") pour "enseigner" à un petit modèle (l'"Élève") comment prédire. Le petit modèle apprend à imiter le grand modèle, atteignant des performances bien supérieures à s'il avait été entraîné seul depuis zéro.

## 4. Frameworks dédiés à l'Edge
Le code Python traditionnel (PyTorch, TensorFlow) est souvent trop lourd pour le déploiement direct.
- **TensorFlow Lite (TFLite)** : Spécialement conçu pour convertir et compresser des modèles TensorFlow afin de les faire tourner sur mobiles et Edge devices (Raspberry, Coral TPU).
- **ONNX Runtime** : Un standard d'interopérabilité (Open Neural Network Exchange) optimisé pour des inférences à grande vitesse sur CPU ARM.
- **TinyML** : Le sous-domaine de l'Edge AI qui s'intéresse au déploiement de modèles sur des puces ultra-basse consommation (de l'ordre du milliwatt).
