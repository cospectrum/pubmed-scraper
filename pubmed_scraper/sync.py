from typing import Optional, Union, Any

from .utils import (
    get_default_headers,
)

from .parser import (
    parse_article_page,
    parse_search_page,
)

from requests import (
    Response,
    Session,
)


def get_response_text(
    url: str, 
    session: Optional[Session] = None,
    **kwargs: Any
) -> str:
    if session is None:
        session = Session()
    if 'headers' not in kwargs:
        kwargs['headers'] = get_default_headers()
    response: Response = session.get(url, **kwargs)
    if response.status_code == 200:
        return response.text
    return ''


def get_search_page(
    term: str, 
    page: Union[str, int] = 1, 
    session: Optional[Session] = None,
    **kwargs: Any
) -> Optional[dict]:
    url = f'https://pubmed.ncbi.nlm.nih.gov/?term={term}&page={page}'
    response_text: str = get_response_text(url=url, session=session, **kwargs)
    return parse_search_page(response_text)


def get_article(
    pmid: Union[str, int],
    session: Optional[Session] = None,
    **kwargs: Any
) -> Optional[dict]:
    url = f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/'
    response_text: str = get_response_text(url=url, session=session, **kwargs)
    return parse_article_page(response_text)

