import sqlite3
import pandas as pd

def main():
    try:
        # 1. Connexion à la base de données SQLite
        conn = sqlite3.connect('database.db')
        print("Connexion à la base de données réussie")

        # 2. Création d'une table et insertion de données si elle n'existe pas
        cursor = conn.cursor()
        
        # Création de la table (si elle n'existe pas)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS produits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            categorie TEXT,
            prix REAL,
            stock INTEGER
        )
        ''')
        
        # Insertion de données exemple (si la table est vide)
        cursor.execute("SELECT COUNT(*) FROM produits")
        if cursor.fetchone()[0] == 0:
            produits_exemple = [
                ('Ordinateur portable', 'Informatique', 899.99, 15),
                ('Smartphone', 'Mobile', 699.99, 30),
                ('Tablette', 'Mobile', 349.99, 20),
                ('Casque audio', 'Audio', 149.99, 45),
                ('Souris sans fil', 'Informatique', 29.99, 100)
            ]
            cursor.executemany("INSERT INTO produits (nom, categorie, prix, stock) VALUES (?, ?, ?, ?)", produits_exemple)
            conn.commit()
            print("Données exemple insérées")

        # 3. Exécution de la requête SQL
        requete = '''
        SELECT id, nom, categorie, prix, stock 
        FROM produits 
        WHERE stock > 0
        ORDER BY prix DESC
        '''
        
        # 4. Chargement des résultats dans un DataFrame
        df = pd.read_sql_query(requete, conn)
        
        # 5. Affichage des 5 premières lignes
        print("\n5 premières lignes du DataFrame :")
        print(df.head())
        
    except sqlite3.Error as e:
        print(f"Erreur SQLite : {e}")
    finally:
        # Fermeture de la connexion
        if conn:
            conn.close()
            print("\nConnexion à la base de données fermée")

if __name__ == "__main__":
    main()