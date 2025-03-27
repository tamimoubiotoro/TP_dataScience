from psaw import PushshiftAPI
import pandas as pd
from datetime import datetime, timedelta

# Initialisation de l'API
api = PushshiftAPI()

def get_reddit_posts(subreddit, limit=10, days_ago=30):
    """Récupère les posts Reddit avec Pushshift"""
    try:
        # Calcul de la date de début
        start_date = int(datetime.now() - timedelta(days=days_ago)).timestamp()
        
        # Requête à l'API
        gen = api.search_submissions(
            subreddit=subreddit,
            limit=limit,
            after=start_date,
            sort='desc',
            sort_type='score'
        )
        
        # Conversion en liste
        posts = list(gen)
        
        # Formatage des données
        posts_data = []
        for post in posts:
            posts_data.append([
                post.title,
                post.score,
                post.num_comments,
                f"https://reddit.com{post.permalink}",
                datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d'),
                post.author
            ])
        
        # Création du DataFrame
        columns = ['Titre', 'Upvotes', 'Commentaires', 'URL', 'Date', 'Auteur']
        return pd.DataFrame(posts_data, columns=columns)
    
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return None

if __name__ == "__main__":
    # Installation nécessaire (décommentez pour installer)
    # !pip install psaw
    
    # Paramètres
    SUBREDDIT = "python"
    LIMIT = 5
    
    print(f"Récupération des {LIMIT} derniers posts de /r/{SUBREDDIT}...")
    df = get_reddit_posts(SUBREDDIT, limit=LIMIT)
    
    if df is not None:
        print("\nRésultats :")
        print(df)
        
        # Sauvegarde en CSV
        filename = f"reddit_{SUBREDDIT}_posts.csv"
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"\nDonnées sauvegardées dans {filename}")
    else:
        print("Aucune donnée récupérée")