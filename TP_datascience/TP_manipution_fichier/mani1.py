import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# 1. Chargement des données
try:
    df = pd.read_excel('employes_dataset.xlsx')
    print("Données chargées avec succès.")
except Exception as e:
    print(f"Erreur lors du chargement du fichier : {e}")
    exit()

# 2. Afficher les 10 premières lignes
print("\n10 premières lignes:")
print(df.head(10))

# 3. Afficher les noms de colonnes
print("\nNoms de colonnes:")
print(df.columns.tolist())

# 4. Compter hommes/femmes - correction pour gérer les valeurs manquantes
if 'Sexe' in df.columns:
    gender_counts = df['Sexe'].value_counts(dropna=False)
    print("\nNombre d'hommes et femmes:")
    print(gender_counts)
else:
    print("\nLa colonne 'Sexe' n'existe pas dans le dataframe")

# 5. Pays les plus représentés - avec gestion des NaN
if 'Pays' in df.columns:
    top_countries = df['Pays'].value_counts(dropna=False).head(5)
    print("\n5 pays les plus représentés:")
    print(top_countries)
else:
    print("\nLa colonne 'Pays' n'existe pas dans le dataframe")

# 6. Statistiques salariales avec NumPy - avec vérification et gestion des NaN
if 'Salaire (€)' in df.columns:
    print("\nStatistiques salariales:")
    print(f"Moyenne: {np.nanmean(df['Salaire (€)']):.2f}")
    print(f"Médiane: {np.nanmedian(df['Salaire (€)']):.2f}")
    print(f"Min: {np.nanmin(df['Salaire (€)']):.2f}")
    print(f"Max: {np.nanmax(df['Salaire (€)']):.2f}")
    print(f"Écart-type: {np.nanstd(df['Salaire (€)']):.2f}")
else:
    print("\nLa colonne 'Salaire (€)' n'existe pas dans le dataframe")

# 7. Âge moyen par département - avec vérification
if all(col in df.columns for col in ['Département', 'Âge']):
    age_by_dept = df.groupby('Département')['Âge'].mean()
    print("\nÂge moyen par département:")
    print(age_by_dept)
else:
    print("\nLes colonnes 'Département' ou 'Âge' manquent")

# 8. Ville avec le plus d'employés - avec vérification
if 'Ville' in df.columns:
    top_city = df['Ville'].mode()[0]  # Utilisation de mode() pour gérer les égalités
    print(f"\nVille avec le plus d'employés: {top_city}")
else:
    print("\nLa colonne 'Ville' n'existe pas dans le dataframe")

# 9. 10 employés les mieux payés - avec vérification
if 'Salaire (€)' in df.columns:
    top_salaries = df.nlargest(10, 'Salaire (€)')[['Nom', 'Prénom', 'Salaire (€)']]
    print("\n10 employés les mieux payés:")
    print(top_salaries)
else:
    print("\nLa colonne 'Salaire (€)' n'existe pas dans le dataframe")

# 10. Employés par département et sexe - avec vérification
if all(col in df.columns for col in ['Département', 'Sexe']):
    dept_gender_counts = df.groupby(['Département', 'Sexe']).size().unstack(fill_value=0)
    print("\nEmployés par département et sexe:")
    print(dept_gender_counts)
else:
    print("\nLes colonnes 'Département' ou 'Sexe' manquent")

# 11. Distribution des âges (graphique) - avec vérification
if 'Âge' in df.columns:
    plt.figure(figsize=(10,6))
    sns.histplot(df['Âge'].dropna(), bins=20, kde=True)
    plt.title('Distribution des âges')
    plt.xlabel('Âge')
    plt.ylabel('Nombre d\'employés')
    plt.show()
else:
    print("\nLa colonne 'Âge' n'existe pas dans le dataframe")

# 12. Colonnes avec valeurs manquantes
missing_cols = df.columns[df.isnull().any()].tolist()
print("\nColonnes avec valeurs manquantes:")
print(missing_cols)

# 13. Remplacer NaN dans Télétravail (%) par la moyenne - avec vérification
if 'Télétravail (%)' in df.columns:
    df['Télétravail (%)'] = df['Télétravail (%)'].fillna(df['Télétravail (%)'].mean())
    print("\nValeurs manquantes dans 'Télétravail (%)' remplacées par la moyenne")
else:
    print("\nLa colonne 'Télétravail (%)' n'existe pas dans le dataframe")

# 14. Remplacer NaN dans Performance (Note) par moyenne par département - avec vérification
if all(col in df.columns for col in ['Performance (Note)', 'Département']):
    df['Performance (Note)'] = df.groupby('Département')['Performance (Note)'].transform(
        lambda x: x.fillna(x.mean()))
    print("Valeurs manquantes dans 'Performance (Note)' remplacées par la moyenne par département")
else:
    print("\nLes colonnes 'Performance (Note)' ou 'Département' manquent")

# 15. Supprimer les lignes avec Salaire manquant - avec vérification
if 'Salaire (€)' in df.columns:
    df = df.dropna(subset=['Salaire (€)'])
    print("Lignes avec salaire manquant supprimées")
else:
    print("\nLa colonne 'Salaire (€)' n'existe pas dans le dataframe")

# 16. Convertir Date d'embauche en datetime - avec vérification
if 'Date d\'embauche' in df.columns:
    df['Date d\'embauche'] = pd.to_datetime(df['Date d\'embauche'], errors='coerce')
    print("Colonne 'Date d\'embauche' convertie en datetime")
else:
    print("\nLa colonne 'Date d\'embauche' n'existe pas dans le dataframe")

# 17. Créer colonne Ancienneté - avec vérification
if 'Date d\'embauche' in df.columns:
    df['Ancienneté (années)'] = (datetime.now() - df['Date d\'embauche']).dt.days / 365.25
    print("Colonne 'Ancienneté (années)' créée")
else:
    print("\nImpossible de créer la colonne 'Ancienneté' - 'Date d\'embauche' manquante")

# 18. Supprimer les doublons
initial_rows = len(df)
df = df.drop_duplicates()
final_rows = len(df)
print(f"\nDoublons supprimés: {initial_rows - final_rows} lignes enlevées")

# 19. Uniformiser les majuscules - avec vérification
text_cols = ['Nom', 'Prénom', 'Ville', 'Pays']
text_cols = [col for col in text_cols if col in df.columns]  # Filtrer les colonnes existantes

if text_cols:
    df[text_cols] = df[text_cols].apply(lambda x: x.str.title() if x.dtype == 'object' else x)
    print("Majuscules uniformisées dans les colonnes textuelles")
else:
    print("\nAucune colonne textuelle trouvée pour uniformiser les majuscules")

# 20. Vérifier emails valides - avec vérification
if 'Email' in df.columns:
    df['Email valide'] = df['Email'].str.match(r'^[^@]+@[^@]+\.[^@]+$')
    invalid_emails = len(df[~df['Email valide']])
    print(f"\nEmails vérifiés: {invalid_emails} emails invalides trouvés")
else:
    print("\nLa colonne 'Email' n'existe pas dans le dataframe")

# 21. Suppression des outliers salariaux avec IQR - avec vérification
if 'Salaire (€)' in df.columns:
    Q1 = df['Salaire (€)'].quantile(0.25)
    Q3 = df['Salaire (€)'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    initial_count = len(df)
    df = df[(df['Salaire (€)'] >= lower_bound) & (df['Salaire (€)'] <= upper_bound)]
    removed_count = initial_count - len(df)
    print(f"\n{removed_count} outliers salariaux supprimés (méthode IQR)")
else:
    print("\nLa colonne 'Salaire (€)' n'existe pas dans le dataframe")

# 22. Test de normalité des âges - avec vérification
if 'Âge' in df.columns:
    from scipy.stats import shapiro
    stat, p = shapiro(df['Âge'].dropna())
    print(f"\nTest de Shapiro-Wilk pour la normalité des âges: p-value={p:.3f}")
    print("La distribution semble normale" if p > 0.05 else "La distribution ne semble pas normale")
else:
    print("\nLa colonne 'Âge' n'existe pas dans le dataframe")

# 23. Colonne prime - avec vérification
if all(col in df.columns for col in ['Performance (Note)', 'Ancienneté (années)']):
    df['Prime'] = np.where((df['Performance (Note)'] >= 4) & (df['Ancienneté (années)'] >= 5), 1000, 0)
    print("\nColonne 'Prime' créée")
else:
    print("\nImpossible de créer la colonne 'Prime' - colonnes requises manquantes")

# 24. Encodage du sexe - avec vérification
if 'Sexe' in df.columns:
    df['Sexe_encoded'] = df['Sexe'].map({'Femme': 0, 'Homme': 1})
    print("Colonne 'Sexe_encoded' créée")
else:
    print("\nLa colonne 'Sexe' n'existe pas dans le dataframe")

# 25. Tranches d'âge - avec vérification
if 'Âge' in df.columns:
    bins = [0, 25, 30, 40, df['Âge'].max()]
    labels = ['0-25', '26-30', '31-40', '40+']
    df['Tranche d\'âge'] = pd.cut(df['Âge'], bins=bins, labels=labels)
    print("Colonne 'Tranche d\'âge' créée")
else:
    print("\nLa colonne 'Âge' n'existe pas dans le dataframe")

# 26. Colonne de langages fictive - modification pour éviter l'avertissement
if len(df) >= 4:
    df.loc[:3, 'Langages'] = ['Python,SQL', 'Java,JavaScript', 'R,Python', 'SQL']
    df_exp = df.copy()
    df_exp['Langages'] = df_exp['Langages'].str.split(',')
    df_exp = df_exp.explode('Langages')
    print("\nColonne 'Langages' créée pour les 4 premiers employés")
else:
    print("\nPas assez de lignes pour créer la colonne 'Langages'")

# 27. MultiIndex - avec vérification
if all(col in df.columns for col in ['Département', 'Sexe']):
    multi_df = df.set_index(['Département', 'Sexe'])
    print("\nDataFrame avec MultiIndex créé")
else:
    print("\nImpossible de créer le MultiIndex - colonnes requises manquantes")

# 28. DataFrame des outliers salariaux - avec vérification
if 'Salaire (€)' in df.columns:
    Q1 = df['Salaire (€)'].quantile(0.25)
    Q3 = df['Salaire (€)'].quantile(0.75)
    IQR = Q3 - Q1
    outliers_df = df[(df['Salaire (€)'] < (Q1 - 1.5 * IQR)) | (df['Salaire (€)'] > (Q3 + 1.5 * IQR))]
    print(f"\nDataFrame des outliers salariaux créé ({len(outliers_df)} lignes)")
else:
    print("\nImpossible de créer le DataFrame des outliers - colonne 'Salaire (€)' manquante")

# 29. Encodage one-hot des départements - avec vérification
if 'Département' in df.columns:
    dept_dummies = pd.get_dummies(df['Département'], prefix='Dept')
    df = pd.concat([df, dept_dummies], axis=1)
    print("\nEncodage one-hot des départements effectué")
else:
    print("\nLa colonne 'Département' n'existe pas dans le dataframe")

# 30. Colonnes date fictives
df['Date inscription'] = pd.date_range(start='1/1/2010', periods=len(df), freq='ME')
df['Année inscription'] = df['Date inscription'].dt.year
df['Mois inscription'] = df['Date inscription'].dt.month
print("\nColonnes de date fictives créées")

# Visualisations avancées
# Boxplot des salaires par département - avec vérification
if all(col in df.columns for col in ['Département', 'Salaire (€)']):
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=df, x='Département', y='Salaire (€)')
    plt.title('Distribution des salaires par département')
    plt.xticks(rotation=45)
    plt.show()
    print("\nle boxplot créer - colonnes requises manquantes")
else:
    print("\nImpossible de créer le boxplot - colonnes requises manquantes")

# Matrice de corrélation - avec vérification
numeric_cols = ['Âge', 'Salaire (€)', 'Performance (Note)', 'Télétravail (%)', 'Ancienneté (années)']
numeric_cols = [col for col in numeric_cols if col in df.columns]

if len(numeric_cols) >= 2:
    corr_matrix = df[numeric_cols].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Matrice de corrélation')
    plt.show()
    print("\nla matrice de corrélation créer")
else:
    print("\nPas assez de colonnes numériques pour créer la matrice de corrélation")

# Sauvegarde finale
try:
    df.to_excel('employes_nettoyé.xlsx', index=False)
    print("\nDataFrame nettoyé sauvegardé avec succès dans 'employes_nettoyé.xlsx'")
except Exception as e:
    print(f"\nErreur lors de la sauvegarde : {e}")
