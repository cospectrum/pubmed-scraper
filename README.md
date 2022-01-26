# PubMed Scraper

Scrape PubMed without an API.


## Usage

### Sync

```python
from pubmed_scraper.sync import get_search_page, get_article

articles = get_search_page(term='covid', page=1)['articles']

for article in articles:
    pmid = article['pmid']
    full_article = get_article(pmid)    
    
    title = full_article['title']
    abstract = full_article['abstract'] 
```

