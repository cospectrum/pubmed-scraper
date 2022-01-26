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


def get_response(
    url: str, 
    session: Optional[Session] = None,
    **kwargs: Any
) -> Response:
    if session is None:
        session = Session()
    if 'headers' not in kwargs:
        kwargs['headers'] = get_default_headers()
    return session.get(url, **kwargs)


def get_search_page(
    term: str, 
    page: Union[str, int] = 1, 
    session: Optional[Session] = None,
    **kwargs: Any
) -> Optional[dict]:
    url = f'https://pubmed.ncbi.nlm.nih.gov/?term={term}&page={page}'
    response: Response = get_response(url=url, session=session, **kwargs)
    if response.status_code != 200:
        return None
    return parse_search_page(response.text)


def get_article(
    pmid: Union[str, int],
    session: Optional[Session] = None,
    **kwargs: Any
) -> Optional[dict]:
    url = f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/'
    response: Response = get_response(url=url, session=session, **kwargs)
    if response.status_code != 200:
        return None
    return parse_article_page(response.text)

