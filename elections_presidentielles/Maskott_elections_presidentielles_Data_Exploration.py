#!/usr/bin/env python
# coding: utf-8

# # Elections présidentielles

# ## 0. Import des bibliothèques, des données et settings

# ### Import des bibliothèques

# Datasets analysis libraries 
import pandas as pd
import numpy as np

# Data visualization libraries
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm

# math library
import math
import statistics

# warning management library
import warnings

# DOS like library
import os

# nan visualization
import missingno as msno


# ### Gestion des warnings

# In[2]:


warnings.filterwarnings('ignore')
sns.set()
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


# ### Chargement des données

# Le fichier fourni était corrompu, ceclui ci a été trouvé sur le site du gouvernement et converti au format .csv.


data_resultat_path='resultats-par-niveau-burvot-t1-france-entiere_small.csv'

df_results=pd.read_csv(data_resultat_path)

# ## 1. Calcul du taux d'abstention moyen par département


df_results_dep_votants=df_results.groupby('Code du département')['Inscrits'].sum()



df_results_dep_abstention=df_results.groupby('Code du département')['Abstentions'].sum()


df_abstention_pc=(df_results_dep_abstention/df_results_dep_votants)*100


# ### Taux d'abstension moyen par département


print("pourcentage d'abstention par département :\n",df_abstention_pc)


# ## 2. Question 2 : calcul des dix circonscriptions pour lesquelles chaque candidat a obtenu le plus de voix

# ### calcul des dix circonscription pour lesquelles M. Arthaud a obtenu le plus de voix

print("\n\n10 cirsconscription pour lesquels chaque candidat a obtenu le plus de voix : \n")


def classement_circonscription(nom_colonne):
    df_results_candidat=df_results.groupby(['Code du département', 'Code de la circonscription'])[nom_colonne].sum()
    df_results_candidat=pd.DataFrame(df_results_candidat)
    return df_results_candidat.sort_values(by=nom_colonne, ascending=False).head(10)

# #### Mme Arthaud

# Verification de la fonction avec Mme Arthaud
df_arthaud=classement_circonscription('Voix')
print("\nARTHAUD \n", df_arthaud, "\n\n")


# #### Résultat pour les autres candidats que Mme Arthaud


# Traitement automatisé pour tous les autres candidats
for col in range(30, 101, 7):
    print(df_results.iloc[1, col])
    col_name='Unnamed: '+str(col+2)
    list_circonscription_candidat=classement_circonscription(col_name)
    list_circonscription_candidat=list_circonscription_candidat.rename(columns={col_name : 'nb de voix'})
    print(list_circonscription_candidat,"\n\n")


# ## Question 3 : Idem pour les suffrages exprimés

# ### le site https://www.linternaute.com/actualite/politique/1188605-abstention-suffrage-exprime-non-inscrits-ca-veut-dire-quoi-le-point-sur-les-definitions/ indique que nombre de voix et suffrages exprimés pour un candidat sont identiques. 

# ## 4. Question 4 :Sélection de 3 colonnes utiles pour prédire le score d'Emmanuel Macron

df_macron=df_results[['Code du département','Exprimés', 'Unnamed: 41']]
df_macron=pd.get_dummies(df_macron, columns=['Code du département'])


y=df_macron['Unnamed: 41']


# y est de type object (string), il faut donc le convertir en float pour être utilisable pour le ML. 
# De plus le séparateur est , au lieu de .
y=y.apply(lambda x: x.replace(',','.'))

y=y.astype(float)

X=df_macron.drop(columns='Unnamed: 41')
# import de sklearn et train_test_split
import sklearn
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test=train_test_split(X, y, test_size=0.4, random_state=0)


#Import du RandomForestRegressor
from sklearn.ensemble import RandomForestRegressor


rfr=RandomForestRegressor(max_depth=10, n_jobs=-1, random_state=0)


rfr.fit(X_train, y_train)


y_pred=rfr.predict(X_test)

# ## 6. Question 6 : Calcul du coefficient de Pearson entre prédictions et valeurs test réelles


y_pred_series=pd.Series(y_pred)


pearson=y_test.corr(y_pred_series)


print ("\n\nCoefficient de pearson pour le modèle RandomForestRegressor avec les 3 colonnes choisies :", pearson)





