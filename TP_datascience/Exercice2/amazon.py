import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuration de Selenium
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
options.add_argument("--window-size=1920,1080")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

try:
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.maximize_window()
except Exception as e:
    print(f"Erreur lors du lancement du navigateur : {e}")
    exit()

# URL de recherche Amazon
url = "https://www.amazon.com/s?k=laptop"

try:
    driver.get(url)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//div[@data-component-type="s-search-result"]'))
    )
    time.sleep(random.uniform(2, 5))
    
    # Faire défiler la page plusieurs fois
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(1, 3))
    
    # Attendre le chargement des produits
    time.sleep(random.uniform(2, 4))
    
    # Extraire les informations des produits
    products = []
    items = driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')
    
    for item in items:
        # Nom du produit
        try:
            name = item.find_element(By.XPATH, './/h2/a/span').text.strip()
        except:
            try:
                name = item.find_element(By.XPATH, './/h2//span').text.strip()
            except:
                name = "Non disponible"
        
        # Prix
        try:
            price = item.find_element(By.XPATH, './/span[@class="a-price"]//span[@class="a-offscreen"]').get_attribute('innerHTML').strip()
        except:
            price = "Non disponible"
        
        # Évaluation
        try:
            rating = item.find_element(By.XPATH, './/span[@class="a-icon-alt"]').get_attribute('innerHTML').strip().replace(' out of 5 stars', '')
        except:
            rating = "Non disponible"
        
        # Lien du produit
        try:
            link = item.find_element(By.XPATH, './/h2/a').get_attribute('href')
        except:
            link = "Non disponible"
        
        products.append([name, price, rating, link])
    
    # Fermer le navigateur
    driver.quit()
    
    # Créer le DataFrame
    df = pd.DataFrame(products, columns=['Produit', 'Prix', 'Avis', 'Lien'])
    
    # Afficher les résultats
    print(df.head(10))
    print(f"\nTotal des produits récupérés : {len(df)}")
    
    # Sauvegarder en CSV
    df.to_csv("amazon_products.csv", index=False, encoding='utf-8-sig')
    print("\nDonnées enregistrées dans 'amazon_products.csv'")

except Exception as e:
    print(f"Une erreur s'est produite : {e}")
    if 'driver' in locals():
        driver.quit()