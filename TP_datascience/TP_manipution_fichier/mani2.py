import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Exercice 2 - E-commerce Transactions
try:
    df_ecom = pd.read_excel('ecommerce_transactions.xlsx')
    print("Données chargées avec succès.")
except Exception as e:
    print(f"Erreur lors du chargement du fichier : {e}")
    exit()

# 1. Aperçu des données
print("\n=== Aperçu des données ===")
print(df_ecom.info())
print("\n5 premières lignes :")
print(df_ecom.head())

# 2. Dimensions et types
print("\n=== Dimensions et types ===")
print(f"Dimensions: {df_ecom.shape}")
print("\nTypes de colonnes:")
print(df_ecom.dtypes)

# 3. Valeurs manquantes
print("\n=== Valeurs manquantes ===")
missing_values = df_ecom.isnull().sum()
print(missing_values[missing_values > 0])

# 4. Supprimer doublons
initial_count = len(df_ecom)
df_ecom = df_ecom.drop_duplicates()
final_count = len(df_ecom)
print(f"\nDoublons supprimés : {initial_count - final_count} lignes enlevées")

# 5. Colonne Année-Mois
if 'Date' in df_ecom.columns:
    try:
        df_ecom['Date'] = pd.to_datetime(df_ecom['Date'], errors='coerce')
        df_ecom['Année-Mois'] = df_ecom['Date'].dt.to_period('M')
        print("\nColonne 'Année-Mois' créée avec succès")
    except Exception as e:
        print(f"\nErreur lors de la création de la colonne Année-Mois : {e}")
else:
    print("\nLa colonne 'Date' est manquante")

# 6. Top 5 pays par CA
if all(col in df_ecom.columns for col in ['Pays', 'Montant total (€)']):
    ca_par_pays = df_ecom.groupby('Pays')['Montant total (€)'].sum().nlargest(5)
    print("\n=== Top 5 pays par chiffre d'affaires ===")
    print(ca_par_pays)
else:
    print("\nColonnes nécessaires pour le calcul du CA par pays manquantes")

# 7. CA par catégorie
if all(col in df_ecom.columns for col in ['Catégorie', 'Montant total (€)']):
    ca_categorie = df_ecom.groupby('Catégorie')['Montant total (€)'].sum().sort_values(ascending=False)
    print("\n=== Chiffre d'affaires par catégorie ===")
    print(ca_categorie)
else:
    print("\nColonnes nécessaires pour le calcul du CA par catégorie manquantes")

# 8. Marques les plus vendues
if all(col in df_ecom.columns for col in ['Catégorie', 'Marque', 'Quantité']):
    try:
        top_marques = df_ecom.groupby(['Catégorie', 'Marque'])['Quantité'].sum().groupby('Catégorie').nlargest(1)
        print("\n=== Marques les plus vendues par catégorie ===")
        print(top_marques)
    except Exception as e:
        print(f"\nErreur lors du calcul des marques les plus vendues : {e}")
else:
    print("\nColonnes nécessaires pour le calcul des marques les plus vendues manquantes")

# 9. Méthodes de paiement par pays
if all(col in df_ecom.columns for col in ['Pays', 'Méthode de paiement']):
    paiement_par_pays = pd.crosstab(df_ecom['Pays'], df_ecom['Méthode de paiement'])
    print("\n=== Méthodes de paiement par pays ===")
    print(paiement_par_pays)
else:
    print("\nColonnes nécessaires pour les méthodes de paiement par pays manquantes")

# 10. Dépense moyenne par client
if all(col in df_ecom.columns for col in ['Client ID', 'Montant total (€)']):
    depense_client = df_ecom.groupby('Client ID')['Montant total (€)'].agg(['mean', 'sum', 'count'])
    top_clients = depense_client.nlargest(10, 'sum')
    print("\n=== Top 10 clients ===")
    print(top_clients)
else:
    print("\nColonnes nécessaires pour le calcul des dépenses clients manquantes")

# 11. Note moyenne par marque et pays
if all(col in df_ecom.columns for col in ['Marque', 'Pays', 'Note']):
    note_moyenne = df_ecom.groupby(['Marque', 'Pays'])['Note'].mean().unstack()
    print("\n=== Note moyenne par marque et pays ===")
    print(note_moyenne)
else:
    print("\nColonnes nécessaires pour le calcul des notes moyennes manquantes")

# 12. Commandes avec note manquante
if 'Note' in df_ecom.columns:
    notes_manquantes = df_ecom[df_ecom['Note'].isna()]
    if not notes_manquantes.empty:
        pattern = notes_manquantes.groupby(['Catégorie', 'Pays']).size().unstack(fill_value=0)
        print("\n=== Répartition des notes manquantes ===")
        print(pattern)
    else:
        print("\nAucune note manquante trouvée")
else:
    print("\nLa colonne 'Note' est manquante")

# 13. Statistiques avec NumPy
if 'Montant total (€)' in df_ecom.columns:
    montants = df_ecom['Montant total (€)'].values
    print("\n=== Statistiques des montants ===")
    print(f"Moyenne: {np.nanmean(montants):.2f}")
    print(f"Médiane: {np.nanmedian(montants):.2f}")
    print(f"Écart-type: {np.nanstd(montants):.2f}")
    print(f"Percentiles (25, 50, 75): {np.nanpercentile(montants, [25, 50, 75])}")
else:
    print("\nLa colonne 'Montant total (€)' est manquante")

# 14. Clients fidèles
if 'Client ID' in df_ecom.columns:
    commandes_par_client = df_ecom['Client ID'].value_counts()
    df_ecom['Client fidèle'] = df_ecom['Client ID'].isin(commandes_par_client[commandes_par_client > 5].index)
    print(f"\nNombre de clients fidèles : {df_ecom['Client fidèle'].sum()}")
else:
    print("\nLa colonne 'Client ID' est manquante")

# Visualisations
try:
    # CA mensuel
    if all(col in df_ecom.columns for col in ['Année-Mois', 'Montant total (€)']):
        plt.figure(figsize=(12, 6))
        df_ecom.groupby('Année-Mois')['Montant total (€)'].sum().plot(kind='bar')
        plt.title('Chiffre d\'affaires mensuel')
        plt.ylabel('Montant total (€)')
        plt.xlabel('Année-Mois')
        plt.tight_layout()
        plt.show()
    
    # Répartition par catégorie
    if 'Catégorie' in df_ecom.columns:
        plt.figure(figsize=(10, 10))
        df_ecom['Catégorie'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Répartition des ventes par catégorie')
        plt.ylabel('')
        plt.tight_layout()
        plt.show()
    
    # Boxplot méthode de paiement
    if all(col in df_ecom.columns for col in ['Méthode de paiement', 'Montant total (€)']):
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df_ecom, x='Méthode de paiement', y='Montant total (€)')
        plt.title('Montant des commandes par méthode de paiement')
        plt.tight_layout()
        plt.show()
except Exception as e:
    print(f"\nErreur lors de la création des visualisations : {e}")

# Sauvegarde finale
try:
    df_ecom.to_excel('ecommerce_transactions_clean.xlsx', index=False)
    print("\nFichier nettoyé sauvegardé avec succès sous 'ecommerce_transactions_clean.xlsx'")
except Exception as e:
    print(f"\nErreur lors de la sauvegarde : {e}")
