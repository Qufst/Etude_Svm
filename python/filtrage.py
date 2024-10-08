#%% NMF sur une petite base de données construite à la main
import numpy as np
import pandas as pd
from sklearn.decomposition import NMF
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import pairwise_distances
from sklearn.metrics import silhouette_score
from fancyimpute import SoftImpute
from sklearn.decomposition import TruncatedSVD
import time as time  

#%% Création d'un dataframe à partir des données d'introduction

data = {
    'Users': [
        'User 1', 'User 2', 'User 3', 'User 4',
        'User 5', 'User 6', 'User 7'
    ],
    'The Walking Dead': [3, 3, 1, 'NA', 'NA', 3, 2],
    'The Witcher': [3, 'NA', 2, 'NA', 3, 1, 3],
    'Dark': ['NA', 'NA', 'NA', 5, 4, 'NA', 4],
    'Gossip Girl': [2, 3, 5, 3, 'NA', 4, 'NA'],
    'The Crown': [3, 1, 2, 2, 'NA', 'NA', 4]
}

df = pd.DataFrame(data)
#Remplacer les valeurs manquantes par 0
df = df.replace('NA', 0)

X = df.values[:, 1:]
X=X.astype(float)

#%%
# On applique la factorisation de matrice non négative

model=NMF(n_components=2, init='random', random_state=0)
W=model.fit_transform(X)
H=model.components_
X_nmf = np.dot (W , H )
print (" Matrice X reconstruite : \n", X_nmf )

# On calucule l'erreur de reconstruction

erreur_nmf= np.sqrt(np.mean((X-X_nmf)**2))

#%%

# On affiche les matrices W et H

print("Matrice W : \n", W)
print("Matrice H : \n", H)

#%%
# Calculer la matrice de consensus avec distances cosinus
consensus_matrix = 1 - pairwise_distances(W, metric='cosine')

# Créer un DataFrame pour la matrice de consensus
df_consensus = pd.DataFrame(consensus_matrix, index=df['Users'], columns=df['Users'])

# Visualisation de la matrice de consensus
plt.figure(figsize=(10, 8))
sns.heatmap(df_consensus, annot=False, cmap='cividis', cbar=True)
plt.title('Matrice de Consensus ')
plt.xlabel('Utilisateurs')
plt.ylabel('Utilisateurs')
plt.show()
#%%
#Les 3 graphes residus variance et silhouette pour les données jouet


ranks = range(2, 6)  
residuals = []
evar_scores = []
silhouette_scores = []


for r in ranks:
    model = NMF(n_components=r, init='random', random_state=0)
    W = model.fit_transform(X)
    H = model.components_
    X_nmf = np.dot(W, H)
    
    # Calcul de l'erreur de reconstruction
    residual = np.sqrt(np.mean((X - X_nmf) ** 2))
    residuals.append(residual)

    # Calcul de la variance expliquée
    evar = 1 - (np.sum((X - X_nmf) * 2) / np.sum(X * 2))
    evar_scores.append(evar)
    
    # Calcul du score de silhouette
    if r > 1:  # Le score de silhouette nécessite au moins 2 clusters
        silhouette_avg = silhouette_score(X, W.argmax(axis=1))
        silhouette_scores.append(silhouette_avg)
    else:
        silhouette_scores.append(0)
    

# Affichage des résultats
plt.figure(figsize=(20, 6))

# Graphique pour les résidus
plt.subplot(1, 3, 1)
plt.plot(ranks, residuals, marker='o', linestyle='-', color='b', label='Résidus')
plt.xlabel('Rang')
plt.ylabel('Erreur de reconstruction (RMSE)')
plt.title('Évolution des résidus')
plt.grid(True)

# Graphique pour la variance expliquée
plt.subplot(1, 3, 2)
plt.plot(ranks, evar_scores, marker='o', linestyle='-', color='c', label='Variance expliquée')
plt.xlabel('Rang')
plt.ylabel('Variance expliquée')
plt.title('Évolution de la variance expliquée')
plt.grid(True)


# Graphique pour le score de silhouette
plt.subplot(1, 3, 3)
plt.plot(ranks, silhouette_scores, marker='^', linestyle='-', color='y', label='Score de silhouette')
plt.xlabel('Rang')
plt.ylabel('Score de silhouette')
plt.title('Évolution du score de silhouette')
plt.grid(True)


plt.tight_layout()
plt.show()
#%%
# SVD

# Effectuer la décomposition SVD
U, Sigma, Vt = np.linalg.svd(X)

# Sigma est un vecteur, on doit le transformer en matrice diagonale
Sigma_diag = np.diag(Sigma)

# Redimensionnement si nécessaire (U est (7,7), Sigma_diag est (5,5), Vt est (5,5))
X_svd = U[:, :Sigma_diag.shape[0]] @ Sigma_diag @ Vt

# Afficher la matrice reconstruite
print(X_svd)

# Calculer l'erreur de reconstruction
erreur_svd = np.sqrt(np.mean((X - X_svd) ** 2))
print("Erreur de reconstruction : ", erreur_svd)




#%%

# Complétion de la matrice

X_na = df.iloc[:, 1:].replace(0, np.nan)

# Convertir les données en tableau NumPy
X = X_na.values

# Appliquer SoftImpute pour imputer les valeurs manquantes
X_chap = SoftImpute(max_iters=100, verbose=0).fit_transform(X)

print(X_chap)



n_components = 2  # Choisir le nombre de composants, vous pouvez ajuster ce chiffre
model = NMF(n_components=n_components, init='random', random_state=0)
W = model.fit_transform(X_chap)
H = model.components_

# Calculer les scores d'appréciation (reconstruire la matrice)
X_reconstructed = np.dot(W, H)

# Identifier le genre recommandé pour chaque utilisateur
recommended_genres = np.argmax(X_reconstructed, axis=1)
genre_labels = df.columns[1:]  # Les noms des genres
print(X_reconstructed)
# Créer un DataFrame avec les résultats
result_df = pd.DataFrame({
    'Utilisateur': df['Utilisateur'],
    'Série recommandée': genre_labels[recommended_genres],
    'Score d\'appréciation': np.max(X_reconstructed, axis=1)  # Scores d'appréciation correspondants
})


print(result_df)

