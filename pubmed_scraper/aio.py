import asyncio
from typing import Optional, Union, Any, Sequence, List


from .utils import (
    get_default_headers,
)


from .parser import (
    parse_article_page,
    parse_search_page,
)

from aiohttp import (
    ClientResponse,
    ClientSession,
)


async def get_response_text(
    url: str,
    session: Optional[ClientSession] = None,
    **kwargs: Any
) -> ClientResponse:
    if session is None:
        async with ClientSession() as _session:
            async with _session.get(url, **kwargs) as response:
                text = await response.text()
                return text
    async with session.get(url, **kwargs) as response:
        text = await response.text()
        return text


async def get_search_page(
    term: str,
    page: Union[str, int] = 1,
    session: Optional[ClientSession] = None,
    **kwargs: Any
) -> Optional[dict]:
    url = f'https://pubmed.ncbi.nlm.nih.gov/?term={term}&page={page}'
    response_text: str = await get_response_text(url=url, session=session, **kwargs)
    return parse_search_page(response_text)


async def get_article(
    pmid: Union[str, int],
    session: Optional[ClientSession] = None,
    **kwargs: Any
) -> Optional[dict]:
    url = f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/'
    response_text: str = await get_response_text(url=url, session=session, **kwargs)
    return parse_article_page(response_text)


async def get_articles(
    pmids: Sequence[Union[str, int]],
    session: Optional[ClientSession] = None,
    **kwargs: Any
) -> List[dict]:
    coros = (get_article(pmid, session=session, **kwargs) for pmid in pmids)
    articles = await asyncio.gather(*coros)
    return articles

