from googlesearch import search
import pandas as pd

# Recherche Google
query = "Python programming"
results = search(query, num=10, stop=10, pause=2)

# Conversion en DataFrame
df = pd.DataFrame(results, columns=['Résultats de recherche'])
print(df)