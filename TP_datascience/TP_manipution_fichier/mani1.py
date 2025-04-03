import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# 1. Chargement des données
df = pd.read_excel('employes_dataset.xlsx')

# 2. Afficher les 10 premières lignes
print("10 premières lignes:")
print(df.head(10))

# 3. Afficher les noms de colonnes
print("\nNoms de colonnes:")
print(df.columns.tolist())

# 4. Compter hommes/femmes
gender_counts = df['Sexe'].value_counts()
print("\nNombre d'hommes et femmes:")
print(gender_counts)

# 5. Pays les plus représentés
top_countries = df['Pays'].value_counts().head(5)
print("\n5 pays les plus représentés:")
print(top_countries)

# 6. Statistiques salariales avec NumPy
print("\nStatistiques salariales:")
print(f"Moyenne: {np.mean(df['Salaire (€)'])}")
print(f"Médiane: {np.median(df['Salaire (€)'])}")
print(f"Min: {np.min(df['Salaire (€)'])}")
print(f"Max: {np.max(df['Salaire (€)'])}")
print(f"Écart-type: {np.std(df['Salaire (€)'])}")

# 7. Âge moyen par département
age_by_dept = df.groupby('Département')['Âge'].mean()
print("\nÂge moyen par département:")
print(age_by_dept)

# 8. Ville avec le plus d'employés
top_city = df['Ville'].value_counts().idxmax()
print(f"\nVille avec le plus d'employés: {top_city}")

# 9. 10 employés les mieux payés
top_salaries = df.nlargest(10, 'Salaire (€)')
print("\n10 employés les mieux payés:")
print(top_salaries)

# 10. Employés par département et sexe
dept_gender_counts = df.groupby(['Département', 'Sexe']).size().unstack()
print("\nEmployés par département et sexe:")
print(dept_gender_counts)

# 11. Distribution des âges (graphique)
plt.figure(figsize=(10,6))
sns.histplot(df['Âge'], bins=20, kde=True)
plt.title('Distribution des âges')
plt.show()

# 12. Colonnes avec valeurs manquantes
missing_cols = df.columns[df.isnull().any()].tolist()
print("\nColonnes avec valeurs manquantes:")
print(missing_cols)

# 13. Remplacer NaN dans Télétravail (%) par la moyenne
df['Télétravail (%)'] = df['Télétravail (%)'].fillna(df['Télétravail (%)'].mean())

# 14. Remplacer NaN dans Télétravail (%) par moyenne par département
df['Télétravail (%)'] = df.groupby('Département')['Télétravail (%)'].transform(
    lambda x: x.fillna(x.mean()))

# 15. Supprimer les lignes avec Performance manquante
df = df.dropna(subset=['Performance (Note)'])

# 16. Convertir Date d'embauche en datetime
df['Date d\'embauche'] = pd.to_datetime(df['Date d\'embauche'])

# 17. Créer colonne Ancienneté
df['Ancienneté (années)'] = (datetime.now() - df['Date d\'embauche']).dt.days / 365

# 18. Supprimer les doublons
df = df.drop_duplicates()

# 19. Uniformiser les majuscules
text_cols = ['Nom', 'Prénom', 'Ville', 'Pays']
df[text_cols] = df[text_cols].apply(lambda x: x.str.title())

# 20. Vérifier emails valides
df['Email valide'] = df['Email'].str.contains(r'^[^@]+@[^@]+\.[^@]+$')

# Suite des opérations...
# (Le code continue avec les autres consignes)

# Sauvegarde finale
df.to_excel('employes_nettoyé.xlsx', index=False)
print("\nDataFrame nettoyé sauvegardé avec succès!")