import pytest

from pubmed_scraper.sync import (
    get_search_page,
    get_article,
)


@pytest.fixture()
def search_page():
    return get_search_page(term='covid', page=1)


def test_get_search_page(requests_session):
    sessions = (None, requests_session)
    for session in sessions:
        page = get_search_page(term='covid', page=1, session=session)
        assert page != dict()
        assert isinstance(page['total-pages'], int)
        assert isinstance(page['results-amount'], int)
        assert page['articles'] != []


def test_get_article(search_page, requests_session):
    pmids = [article['pmid'] for article in search_page['articles']]
    assert pmids != []
    sessions = (None, requests_session)
    for session in sessions:
        for pmid in pmids:
            article = get_article(pmid, session=session)
            assert article['title'] != ''
            assert article['abstract'] != ''
            assert article['authors'] != []
