import pandas as pd

# Exercice 2 - E-commerce Transactions
df_ecom = pd.read_excel('ecommerce_transactions.xlsx')

# 1. Aperçu des données
print(df_ecom.info())
print(df_ecom.head())

# 2. Dimensions et types
print(f"\nDimensions: {df_ecom.shape}")
print("\nTypes de colonnes:")
print(df_ecom.dtypes)

# 3. Valeurs manquantes
print("\nValeurs manquantes par colonne:")
print(df_ecom.isnull().sum())

# 4. Supprimer doublons
df_ecom = df_ecom.drop_duplicates()

# 5. Colonne Année-Mois
df_ecom['Date'] = pd.to_datetime(df_ecom['Date'])
df_ecom['Année-Mois'] = df_ecom['Date'].dt.to_period('M')

# 6. Top 5 pays par CA
ca_par_pays = df_ecom.groupby('Pays')['Montant total (€)'].sum().nlargest(5)
print("\nTop 5 pays par chiffre d'affaires:")
print(ca_par_pays)

# Suite des opérations...
# (Le code continue avec les autres consignes)

# Sauvegarde finale
df_ecom.to_excel('ecommerce_transactions_clean.xlsx', index=False)