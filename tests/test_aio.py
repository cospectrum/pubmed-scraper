import pytest
import pytest_asyncio
from pubmed_scraper.aio import (
    get_search_page,
    get_articles,
)


@pytest_asyncio.fixture
async def search_page(aiohttp_session):
    page = await get_search_page(term='covid', page=1, session=aiohttp_session)
    return page


@pytest.mark.asyncio
async def test_get_search_page(aiohttp_session):
    sessions = (None, aiohttp_session)
    for session in sessions:
        page = await get_search_page(term='covid', page=1, session=session)
        assert page != dict()
        assert isinstance(page['total-pages'], int)
        assert isinstance(page['results-amount'], int)
        assert page['articles'] != []


@pytest.mark.asyncio
async def test_get_article(search_page, aiohttp_session):
    pmids = [article['pmid'] for article in search_page['articles']]
    assert pmids != []
    sessions = (None, aiohttp_session)
    for session in sessions:
        full_articles = await get_articles(pmids, session=session, timeout=10)
        for article in full_articles:
            assert article['title'] != ''
            assert article['abstract'] != ''
            assert article['authors'] != []

