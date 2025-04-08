import requests
import pandas as pd

# Remplacez par vos identifiants réels
ACCESS_TOKEN = "VOTRE_ACCESS_TOKEN"
USER_ID = "VOTRE_USER_ID"

def fetch_instagram_data(access_token, user_id):
    url = (
        f"https://graph.instagram.com/{user_id}/media"
        f"?fields=id,caption,like_count,media_url"
        f"&access_token={access_token}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Vérification que 'data' est présent dans la réponse
        if 'data' not in data:
            print("Erreur : La réponse ne contient pas de clé 'data'.")
            print("Réponse brute :", data)
            return None

        instagram_data = []
        for post in data['data']:
            caption = post.get('caption')
            likes = post.get('like_count')
            media_url = post.get('media_url')

            if caption is not None and likes is not None and media_url is not None:
                instagram_data.append([caption, likes, media_url])
            else:
                print(f"Données incomplètes pour le post ID: {post.get('id', 'Inconnu')} — Ignoré.")

        return instagram_data

    except requests.exceptions.RequestException as e:
        print(f"Erreur de requête : {e}")
    except ValueError as e:
        print(f"Erreur de décodage JSON : {e}")
        print("Réponse brute :", response.text)
    return None

def main():
    data = fetch_instagram_data(ACCESS_TOKEN, USER_ID)
    if data:
        df = pd.DataFrame(data, columns=['Caption', 'Likes', 'Image URL'])
        print(df)
    else:
        print("Aucune donnée à afficher.")

if __name__ == "__main__":
    main()
