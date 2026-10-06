# Document D10 : Architectures Deep Learning et Modèles Avancés

## 1. Vue d'ensemble des Modèles IA en Maintenance
La maintenance prédictive s'appuie sur deux grandes familles d'algorithmes : les méthodes classiques (Machine Learning) et les réseaux de neurones (Deep Learning). Le choix du modèle dépend des ressources de calcul, de la latence exigée et de la quantité de données étiquetées disponibles.

## 2. Modèles Non-Supervisés : L'Autoencodeur (Autoencoder)
L'Autoencodeur est un réseau de neurones artificiels conçu pour la compression et la reconstruction de données. 
- **Fonctionnement** : Il est composé d'un encodeur qui réduit la dimensionnalité des données d'entrée vers un espace latent ("bottleneck"), et d'un décodeur qui tente de reconstruire l'entrée originale.
- **Utilisation en détection d'anomalies** : On entraîne l'Autoencodeur UNIQUEMENT sur des données saines. Ainsi, il devient un expert pour reconstruire des signaux normaux. Lorsqu'on lui soumet un signal d'anomalie (vibrations d'un roulement défectueux), il n'arrive pas à le reconstruire correctement. L'erreur de reconstruction (MSE - Mean Squared Error) explose, ce qui déclenche l'alarme.
- **Avantages** : Ne nécessite pas de données de pannes (qui sont très rares en milieu industriel).

## 3. Modèles Supervisés : Le CNN 1D (Réseau de Neurones Convolutif 1D)
Si les CNN sont célèbres pour l'analyse d'images (CNN 2D), ils sont tout aussi puissants pour les séries temporelles et les signaux via des convolutions en une dimension (CNN 1D).
- **Extraction de caractéristiques spatiales temporelles** : Les filtres convolutifs se déplacent le long de la série temporelle ou du spectre FFT pour détecter des "motifs" locaux, tels que des pics d'énergie répétitifs (les chocs d'un roulement endommagé).
- **Architecture classique** : Une succession de couches `Conv1d` (pour trouver les motifs), suivies de couches `MaxPool1d` (pour réduire la dimensionnalité) et enfin de couches denses (Fully Connected) pour la classification finale (Normal vs Anomalie).
- **Performances** : Le CNN 1D est extrêmement précis, mais nécessite des données étiquetées (données de machines saines ET en panne) pour s'entraîner correctement.

## 4. Machine Learning Classique (Edge Friendly)
Pour les environnements avec très peu de mémoire (comme les microcontrôleurs), les réseaux de neurones sont parfois trop gourmands.
- **Random Forest** : Ensemble d'arbres de décision. Il est robuste, insensible au sur-apprentissage et s'exécute extrêmement vite en inférence, ce qui le rend parfait pour le Edge Computing.
- **Isolation Forest** : Méthode non-supervisée très performante. Contrairement aux approches qui essaient de modéliser le comportement normal, l'Isolation Forest cherche directement à "isoler" les points de données les plus étranges en effectuant des coupes aléatoires. Les anomalies nécessitent très peu de coupes pour être isolées de la masse.

## 5. Explicabilité (XAI - eXplainable AI)
L'un des défis du Deep Learning est son aspect "boîte noire". Sur un site industriel, un opérateur refusera d'arrêter une machine de plusieurs millions d'euros simplement parce que "l'IA l'a dit".
- Des techniques comme SHAP (SHapley Additive exPlanations) ou l'importance des caractéristiques de Gini dans les arbres de décision permettent de "tracer" les prédictions.
- Par exemple, l'IA indique une anomalie, et l'explicabilité nous montre que c'est le "Kurtosis" ou la "Bande de fréquence BPFI" qui a fait pencher la décision, fournissant un diagnostic concret au technicien humain.
