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
        assert page['total-pages'] != 0
        assert page['results-amount'] != 0
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
            for similar_article in article['similar-articles']:
                assert similar_article['authors'] != ''
                assert similar_article['cite'] != ''
            for cited_by_article in article['cited-by-articles']:
                assert cited_by_article['authors'] != ''
                assert cited_by_article['cite'] != ''
