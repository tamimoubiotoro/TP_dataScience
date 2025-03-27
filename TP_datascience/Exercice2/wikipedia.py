import wikipediaapi

headers={
    "User-Agent":"projet/1.0 (torotam07@gmail.com)"
}
language='fr'
wiki_wiki = wikipediaapi.Wikipedia(user_agent='projet/1.0 (torotam07@gmail.com)').page("data")
print(wiki_wiki.text)