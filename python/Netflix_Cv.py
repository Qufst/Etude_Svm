########################################
######## Base de donnée Netflix ########
########################################

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
#%% NMF données Netflix

file_path = 'C:/Users/qfest/tp_svm/article_nmf_svd/Etude_Svm/data/Netflix_Dataset_Rating.csv'
f = pd.read_csv(file_path)

pivot_df = f.pivot_table(index='User_ID', columns='Movie_ID', values='Rating')
X = pivot_df.values.astype(float)
X = np.nan_to_num(X, nan=0.0)
# Afficher le DataFrame résultant
print(pivot_df.head())
# %%
# print(pivot_df)
X = pivot_df.values.astype(float)
X = np.nan_to_num(X, nan=0.0)
print(X)


#%%
T0 = time.time()

modeldata = NMF(n_components=2, init='random', random_state=0)
W = modeldata.fit_transform(X)
H = modeldata.components_
X_reconstructed = np.dot(W, H)

print(f"Temps d'exécution : {time.time() - T0:.2f} secondes")

# %%
recommended_genres = np.argmax(X_reconstructed, axis=1)
film_labels = pivot_df.columns  # Les identifiants des films
user_ids = pivot_df.index  # Les identifiants des utilisateurs
print(film_labels)
#print(X_reconstructed)
# Créer un DataFrame avec les résultats
result_df = pd.DataFrame({
    'Utilisateur': user_ids,
    'Film recommandé': film_labels[recommended_genres],
    'Score d\'appréciation': np.max(X_reconstructed, axis=1)  # Scores d'appréciation correspondants
})
#print(result_df)
# %%
film_counts = result_df['Film recommandé'].value_counts()

#Calcule de la proportion de reco de chaque film
total_recommendations = len(result_df)
film_proportions = film_counts / total_recommendations

most_recommended_film = film_counts.idxmax()  # Film le plus recommandé
most_recommended_count = film_counts.max()  # Nombre de recommandations
proportion = film_proportions[most_recommended_film]  # Proportion

print(f"Film le plus recommandé : {most_recommended_film}")
print(f"Nombre de recommandations : {most_recommended_count}")
print(f"Proportion : {proportion:.2%}")


#%%
# Compte le nombre de recommandations pour chaque film
film_counts = result_df['Film recommandé'].value_counts()

# Calcule de la proportion de reco de chaque film
total_recommendations = len(result_df)
film_proportions = film_counts / total_recommendations

# Identifie les 3 films les plus recommandés
top_n = 3
most_recommended_films = film_counts.nlargest(top_n)  # Prend les 3 films les plus recommandés
most_recommended_film_names = most_recommended_films.index.tolist()  # Noms des films
most_recommended_counts = most_recommended_films.values.tolist()  # Nombres de recommandations
most_recommended_proportions = film_proportions[most_recommended_film_names].values.tolist()  # Proportions

# Affiche les résultats
for film, count, proportion in zip(most_recommended_film_names, most_recommended_counts, most_recommended_proportions):
    print(f"Film recommandé : {film}")
    print(f"Nombre de recommandations : {count}")
    print(f"Proportion : {proportion:.2%}\n")




#%%


# Charger le dataset des notations de films dans un DataFrame pandas
data = 'C:/Users/qfest/tp_svm/article_nmf_svd/Etude_Svm/data/Netflix_Dataset_Rating.csv'
df = pd.read_csv(data)

# Créer un tableau croisé (pivot) avec les utilisateurs en ligne et les films en colonne, et les notes comme valeurs
pivot_df = df.pivot_table(index='User_ID', columns='Movie_ID', values='Rating')

# Afficher les premières lignes du tableau croisé (pivot table) pour voir sa structure
print(pivot_df.head())

# Convertir le pivot table en un tableau NumPy
X = pivot_df.values.astype(float)

# Remplacer les valeurs NaN  par 0.0 
X = np.nan_to_num(X, nan=0.0)

# Afficher la matrice X convertie
print(X)

# Mesurer le temps d'exécution de la factorisation NMF
T0 = time.time()

# Appliquer de la NMF 

modeldata = NMF(n_components=2, init='random', random_state=0)

# W : matrice des utilisateurs par facteurs
W = modeldata.fit_transform(X)

# H : matrice des facteurs par films
H = modeldata.components_

# Reconstruire la matrice X à partir des matrices W et H (approximation)
X_reconstructed = np.dot(W, H)

# Afficher le temps d'exécution de la factorisation NMF
print(f"Temps d'exécution : {time.time() - T0:.2f} secondes")

# Identifier les genres ou films les plus susceptibles d'être recommandés pour chaque utilisateur
# Cela se fait en trouvant l'indice de la valeur maximale dans chaque ligne de la matrice reconstruite
recommended_genres = np.argmax(X_reconstructed, axis=1)

# Extraire les étiquettes (titres de films) et les identifiants d'utilisateurs
film_labels = pivot_df.columns  # Les identifiants des films (colonnes)
user_ids = pivot_df.index  # Les identifiants des utilisateurs (lignes)

# Afficher les étiquettes de films (les titres ou identifiants de films)
print(film_labels)

# Créer un DataFrame avec les recommandations de films pour chaque utilisateur
result_df = pd.DataFrame({
    'Utilisateur': user_ids,
    'Film recommandé': film_labels[recommended_genres],  # Film avec le score le plus élevé pour chaque utilisateur
    'Score d\'appréciation': np.max(X_reconstructed, axis=1)  # Le score de prédiction maximal pour chaque utilisateur
})

# Afficher le nombre de recommandations pour chaque film
film_counts = result_df['Film recommandé'].value_counts()

# Calculer la proportion de recommandations pour chaque film
total_recommendations = len(result_df)  # Nombre total de recommandations
film_proportions = film_counts / total_recommendations  # Proportion de chaque film recommandé

# Identifier le film le plus recommandé et sa proportion
most_recommended_film = film_counts.idxmax()  # Film avec le plus grand nombre de recommandations
most_recommended_count = film_counts.max()  # Nombre total de recommandations pour ce film
proportion = film_proportions[most_recommended_film]  # Proportion de recommandations pour ce film

# Afficher le film le plus recommandé, le nombre de recommandations et sa proportion
print(f"Film le plus recommandé : {most_recommended_film}")
print(f"Nombre de recommandations : {most_recommended_count}")
print(f"Proportion : {proportion:.2%}")

# Compter le nombre de recommandations pour chaque film
film_counts = result_df['Film recommandé'].value_counts()

# Recalculer la proportion de recommandations pour chaque film
total_recommendations = len(result_df)
film_proportions = film_counts / total_recommendations

# Identifier les 3 films les plus recommandés
top_n = 3  # Nombre de films à afficher
most_recommended_films = film_counts.nlargest(top_n)  # Sélectionner les 3 films les plus recommandés
most_recommended_film_names = most_recommended_films.index.tolist()  # Noms (ou ID) des films les plus recommandés
most_recommended_counts = most_recommended_films.values.tolist()  # Nombre de recommandations pour ces films
most_recommended_proportions = film_proportions[most_recommended_film_names].values.tolist()  # Proportions correspondantes

# Afficher les 3 films les plus recommandés, avec leur nombre de recommandations et proportion
for film, count, proportion in zip(most_recommended_film_names, most_recommended_counts, most_recommended_proportions):
    print(f"Film recommandé : {film}")
    print(f"Nombre de recommandations : {count}")
    print(f"Proportion : {proportion:.2%}\n")
erreur_nmf= np.sqrt(np.mean((X-X_reconstructed)**2))
print(erreur_nmf)

#%% SVD données Netflix

# Appliquer de la SVD

svd = TruncatedSVD(n_components=2)
svd.fit(X)
X_svd = svd.transform(X)
X_reconstructed = X_svd @ svd.components_

# Afficher le temps d'exécution de la factorisation NMF
print(f"Temps d'exécution : {time.time() - T0:.2f} secondes")

# Identifier les genres ou films les plus susceptibles d'être recommandés pour chaque utilisateur
# Cela se fait en trouvant l'indice de la valeur maximale dans chaque ligne de la matrice reconstruite
recommended_genres = np.argmax(X_reconstructed, axis=1)

# Extraire les étiquettes (titres de films) et les identifiants d'utilisateurs
film_labels = pivot_df.columns  # Les identifiants des films (colonnes)
user_ids = pivot_df.index  # Les identifiants des utilisateurs (lignes)

# Afficher les étiquettes de films (les titres ou identifiants de films)
print(film_labels)

# Créer un DataFrame avec les recommandations de films pour chaque utilisateur
result_df = pd.DataFrame({
    'Utilisateur': user_ids,
    'Film recommandé': film_labels[recommended_genres],  # Film avec le score le plus élevé pour chaque utilisateur
    'Score d\'appréciation': np.max(X_reconstructed, axis=1)  # Le score de prédiction maximal pour chaque utilisateur
})

# Afficher le nombre de recommandations pour chaque film
film_counts = result_df['Film recommandé'].value_counts()

# Calculer la proportion de recommandations pour chaque film
total_recommendations = len(result_df)  # Nombre total de recommandations
film_proportions = film_counts / total_recommendations  # Proportion de chaque film recommandé

# Identifier le film le plus recommandé et sa proportion
most_recommended_film = film_counts.idxmax()  # Film avec le plus grand nombre de recommandations
most_recommended_count = film_counts.max()  # Nombre total de recommandations pour ce film
proportion = film_proportions[most_recommended_film]  # Proportion de recommandations pour ce film

# Afficher le film le plus recommandé, le nombre de recommandations et sa proportion
print(f"Film le plus recommandé : {most_recommended_film}")
print(f"Nombre de recommandations : {most_recommended_count}")
print(f"Proportion : {proportion:.2%}")

# Compter le nombre de recommandations pour chaque film
film_counts = result_df['Film recommandé'].value_counts()

# Recalculer la proportion de recommandations pour chaque film
total_recommendations = len(result_df)
film_proportions = film_counts / total_recommendations

# Identifier les 3 films les plus recommandés
top_n = 3  # Nombre de films à afficher
most_recommended_films = film_counts.nlargest(top_n)  # Sélectionner les 3 films les plus recommandés
most_recommended_film_names = most_recommended_films.index.tolist()  # Noms (ou ID) des films les plus recommandés
most_recommended_counts = most_recommended_films.values.tolist()  # Nombre de recommandations pour ces films
most_recommended_proportions = film_proportions[most_recommended_film_names].values.tolist()  # Proportions correspondantes

# Afficher les 3 films les plus recommandés, avec leur nombre de recommandations et proportion
for film, count, proportion in zip(most_recommended_film_names, most_recommended_counts, most_recommended_proportions):
    print(f"Film recommandé : {film}")
    print(f"Nombre de recommandations : {count}")
    print(f"Proportion : {proportion:.2%}\n")

erreur_svd= np.sqrt(np.mean((X-X_reconstructed)**2))
print(erreur_svd)


#%% NMF Cross-va Grosse data Netflix
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.decomposition import NMF
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error, silhouette_score
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Chemin vers le fichier
file_path = 'C:/Users/qfest/tp_svm/article_nmf_svd/Etude_Svm/data/Netflix_Dataset_Rating.csv'

# Lire le fichier CSV dans un DataFrame
f = pd.read_csv(file_path)

# Vérifier les colonnes et créer un tableau croisé dynamique
if 'User_ID' in f.columns and 'Movie_ID' in f.columns and 'Rating' in f.columns:
    pivot_df = f.pivot_table(index='User_ID', columns='Movie_ID', values='Rating')
    X = pivot_df.values.astype(float)
    X = np.nan_to_num(X, nan=0.0)  # Remplacer les valeurs NaN par 0
else:
    print("Les colonnes 'User_ID', 'Movie_ID' ou 'Rating' ne sont pas présentes dans le fichier.")

# Imputation des données manquantes (remplacer les valeurs manquantes par des 0)
imputer = SimpleImputer(strategy='constant')
X_imputed = imputer.fit_transform(X)

# Liste des valeurs à tester pour n_components
n_components_values = [2, 5, 10, 20]

# Configuration de la validation croisée K-Fold
kf = KFold(n_splits=5, shuffle=True, random_state=0)

# Dictionnaires pour stocker les scores MSE et les scores de silhouette pour chaque n_components
mse_scores_train = {}
mse_scores_test = {}
silhouette_scores = {}

# Validation croisée K-Fold pour chaque valeur de n_components
for n_components in n_components_values:
    mse_fold_scores_train = []
    mse_fold_scores_test = []
    silhouette_fold_scores = []
    
    for train_index, test_index in kf.split(X_imputed):
        # Séparer les ensembles d'entraînement et de test
        X_train, X_test = X_imputed[train_index], X_imputed[test_index]
        
        # Ajuster le modèle NMF
        model = NMF(n_components=n_components, init='random', random_state=0)
        W_train = model.fit_transform(X_train)
        H = model.components_
        
        # Reconstruction des ensembles d'entraînement et de test
        X_train_reconstructed = W_train.dot(H)
        X_test_reconstructed = model.transform(X_test).dot(H)
        
        # Calcul des MSE pour l'entraînement et le test
        mse_train = mean_squared_error(X_train, X_train_reconstructed)
        mse_test = mean_squared_error(X_test, X_test_reconstructed)
        
        mse_fold_scores_train.append(mse_train)
        mse_fold_scores_test.append(mse_test)
        
        # Calcul du score de silhouette (nécessite au moins 2 composantes)
        if n_components > 1:
            # Utilisation de KMeans pour extraire des labels de clusters de W_train
            kmeans = KMeans(n_clusters=n_components, random_state=0)
            cluster_labels = kmeans.fit_predict(W_train)

            # Calcul du score de silhouette
            silhouette_avg = silhouette_score(X_train, cluster_labels)
            silhouette_fold_scores.append(silhouette_avg)
    
    # Moyenne des MSE et des scores de silhouette pour cette valeur de n_components
    mse_scores_train[n_components] = np.mean(mse_fold_scores_train)
    mse_scores_test[n_components] = np.mean(mse_fold_scores_test)
    
    if n_components > 1:
        silhouette_scores[n_components] = np.mean(silhouette_fold_scores)

# Graphique 1: Evolution des erreurs MSE pour les ensembles d'entraînement et de test
plt.figure(figsize=(10, 6))
plt.plot(n_components_values, [mse_scores_train[n] for n in n_components_values], marker='o', label='MSE Train', color='b')
plt.plot(n_components_values, [mse_scores_test[n] for n in n_components_values], marker='s', label='MSE Test', color='r')
plt.xlabel('n_components')
plt.ylabel('MSE')
plt.title('Évolution de l\'erreur MSE en fonction de n_components')
plt.legend()
plt.grid(True)
plt.show()

# Graphique 2: Evolution du score de silhouette
if len(silhouette_scores) > 0:
    plt.figure(figsize=(10, 6))
    plt.plot(list(silhouette_scores.keys()), list(silhouette_scores.values()), marker='^', linestyle='-', color='g', label='Score de silhouette')
    plt.xlabel('n_components')
    plt.ylabel('Score de silhouette')
    plt.title('Évolution du score de silhouette en fonction de n_components')
    plt.grid(True)
    plt.show()
else:
    print("Pas assez de composantes pour calculer le score de silhouette.")

#%%
# SVD

import numpy as np
from sklearn.decomposition import TruncatedSVD



# Initialiser et ajuster la décomposition SVD
svd = TruncatedSVD(n_components=2, n_iter=7, random_state=42)
svd.fit(X_imputed)
# Transformer X en espace réduit
X_svd = svd.transform(X_imputed)
# Calculer la matrice reconstruite (approximation de X)
X_reconstructed = X_svd @ svd.components_

# Afficher le produit matriciel
print("Produit matriciel X_svd @ svd.components_ :\n", X_reconstructed)

# Calculer les argmax pour chaque ligne
argmaxs_per_row = np.argmax(X_reconstructed, axis=1)

# Afficher les indices des valeurs maximales (argmax) par ligne
print("Indices des argmax par ligne :", argmaxs_per_row)

# Calculer l'erreur de reconstruction en comparant X à X_reconstructed
erreur_svd = np.sqrt(np.mean((X_imputed - X_reconstructed) ** 2))
print("Erreur de reconstruction : ", erreur_svd)

