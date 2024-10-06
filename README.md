# Introduction à la recommandation par Factorisation ou Complétion

Auteurs: Lahjiouj Aicha, Dias Pierre, Festor Quentin

## Description

L'objectif de ce dépôt est d'étudier les articles suivants:
- [http://www.math.univ-toulouse.fr/~besse/Wikistat/pdf/st-scenar-explo7-nmf.pdf](Introduction aux méthodes)
- [http://wikistat.fr/pdf/st-m-explo-nmf.pdf](Factorisation par matrices non négatives NMF)
- [https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.NMF.html](Codes)

## Organisation du dépôt

- Etude: Les documents relatifs à notre étude sont disponibles dans le dossier 'pdf'
- Source LaTeX: Le fichier LaTeX original utilisé pour générer le rapport se trouve dans le dossier 'tex'
- Codes Python:  Les scripts Python utilisés dans notre étude sont disponibles dans le dossier 'python'

On retrouve les dépendances du projet dans le fichier 'requirements.txt'. les prérequis incluent:
- 'numpy'
- 'pandas'
- 'matplotlib'
- 'scikit-learn' (pour 'NMF' et 'TruncatedSVD')
- 'fancyimpute' (pour 'SoftImpute')

## Compilation du rapport

Pour générer le rapport, un compilateur LaTeX est nécessaire. Vous pouvez utiliser un outil comme Overleaf pour la compilation en ligne.