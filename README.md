# PubMed Scraper

Scrape PubMed without an API.

## Install

```sh
pip install git+https://github.com/cospectrum/pubmed-scraper.git
```

## Usage

### Sync

```python
from pubmed_scraper.sync import get_search_page, get_article

page = get_search_page(term='covid', page=1)

for article in page['articles']:
    pmid = article['pmid']
    full_article = get_article(pmid, timeout=5)    
    
    title = full_article['title']
    abstract = full_article['abstract'] 
```

### Async

```python
import asyncio
from aiohttp import ClientSession
from pubmed_scraper.aio import get_search_page, get_articles


async def main():
    async with ClientSession as session:
        page = await get_search_page(term='cancer', page=1, session=session)
        pmids = [pmid for pmid in page['articles']]
        full_articles = await get_articles(pmids, session=session, timeout=20)
        return full_articles


articles = asyncio.run(main())
```
