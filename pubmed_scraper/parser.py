from typing import Optional

from bs4 import (
    BeautifulSoup,
    Tag,
)


def parse_int(string: str) -> int:
    integer = int(string.replace(',', ''))
    return integer


def parse_results_amount(table_head: Optional[Tag]) -> int:
    if table_head is None:
        return 0
    results_amount_div = table_head.find('div', {'class': 'results-amount'})
    if results_amount_div is None:
        return 0
    results_amount = results_amount_div.span
    if results_amount is None:
        return 0
    return parse_int(results_amount.text)


def parse_total_pages(table_head: Optional[Tag]) -> int:
    if table_head is None:
        return 0
    pagination_div = table_head.find('div', {'class': 'top-pagination'})
    if pagination_div is None:
        return 0
    pagination_label = pagination_div.find('label', {'class': 'of-total-pages'})
    if pagination_label is None:
        return 0
    total_pages = parse_int(pagination_label.text.split()[-1])
    return total_pages


def parse_article_row(article: Tag) -> dict:
    article_tag = article.find('div', {'class': 'docsum-content'})
    if article_tag is None:
        return dict()
    article_data = dict()
    title_tag = article_tag.find('a', {'class': 'docsum-title'})
    if title_tag is None:
        return article_data
    article_data['pmid'] = title_tag.get('href', '').replace('/', '')
    article_data['title'] = title_tag.text.strip()
    
    snippet = article_tag.find('div', {'full-view-snippet'})
    if snippet is not None:
        article_data['snippet'] = ' '.join(
            child.text.strip() for child in snippet.children
        ).lstrip()
    
    citation: Optional[Tag] = article_tag.find(
        'div', {'class': ['docsum-citation', 'full-citation']}
    )
    if citation is None:
        return article_data
    authors_tag = citation.find(
        'span', {'class': ['docsum-authors', 'full-authors']}
    )
    if authors_tag is not None:
        article_data['authors'] = authors_tag.text.strip()
    return article_data


def parse_search_page(html: str) -> dict:
    data = {
        'results-amount': 0,
        'total-pages': 0,
        'articles': [],
    }
    if not html:
        return data
    soup = BeautifulSoup(html, 'html.parser')
    search_results: Optional[Tag] = soup.find('div', {'id': 'search-results'})
    if search_results is None:
        return data
    table_head = search_results.find('div', {'class': 'top-wrapper'})
    data['results-amount']: int = parse_results_amount(table_head)
    data['total-pages']: int = parse_total_pages(table_head)

    articles_table = search_results.find('div', {'class': 'search-results-chunks'})
    if articles_table is None:
        return data
    articles = articles_table.find_all('article')
    data['articles']: list = [parse_article_row(article) for article in articles]
    return data


def parse_article_head(head: Optional[Tag]) -> dict:
    data = {
        'publication-type': '',
        'journal': '',
        'date': '',
        'doi': '',
        'secondary-date': '',
        'title': '',
        'authors': [],
    }
    if head is None:
        return data
    publication_type = head.find('div', {'id': 'publication-type'})
    if publication_type is not None:
        data['publication-type'] = publication_type.text.strip()
    journal = head.find('button', {'id': 'full-view-journal-trigger'})
    if journal is not None:
        data['journal'] = journal.get('title', '')
    date = head.find('span', {'class': 'cit'})
    if date is not None:
        data['date'] = date.text.split(';')[0].strip()
    doi = head.find('span', {'class': 'identifier doi'})
    if doi is not None:
        data['doi'] = doi.a.text.strip()
    secondary_date = head.find('span', {'class': 'secondary-date'})
    if secondary_date is not None:
        data['secondary-date'] = secondary_date.text.strip()
    title = head.find('h1', {'class': 'heading-title'})
    if title is not None:
        data['title'] = title.text.strip()
    authors = head.find('div', {'class': 'authors'})
    if authors is not None:
        authors = authors.find_all('span', {'class': 'authors-list-item'})
        data['authors']: list = [
            {
                'full-name': tag.a.text, 
                'url': 'https://pubmed.ncbi.nlm.nih.gov' + tag.a['href'],
            }
            for tag in authors
        ]
    return data


def parse_articles_list(tag: Optional[Tag]) -> list:
    if tag is None:
        return [] 
    def parse_authors(article: Tag) -> str:
        f_author = lambda x: x.name == 'span' and 'full-authors' in x.get('class', {})
        tag = article.find(f_author)
        if tag is None:
            return ''
        return tag.text
    def parse_cite(article: Tag) -> str:
        f_cite = lambda x: x.name == 'span' and (
            'docsum-journal-citation' in x.get('class', {}) or 
            'full-journal-citation' in x.get('class', {})
        )
        tag = article.find(f_cite)
        if tag is None:
            return ''
        return tag.text
    articles = tag.find_all('li')
    data = [
        {
            'pmid': article.a.get('href', '').replace('/', ''),
            'title': article.a.text.strip(),
            'authors': parse_authors(article),
            'cite': parse_cite(article),
        }
        for article in articles if article.a is not None
    ]
    return data


def parse_references(tag: Optional[Tag]) -> list:
    if tag is None:
        return []
    references = tag.find_all('li', {'class': 'skip-numbering'})
    def parse_text(tag: Tag) -> str:
        children = tag.children
        try:
            text = next(children).text.strip()
        except StopIteration:
            return ''
        right_text = ' '.join(tag.text.strip() for tag in children)
        rindex = text.rfind('-')
        if rindex != -1:
            chars = tuple(text)
            left_chars = ''.join(chars[:rindex]).rstrip()
            right_chars = ''.join(chars[rindex + 1:])
            text = f'{left_chars} -{right_chars}'
        return f'{text} {right_text}'.rstrip()
    def parse_href(tag: Tag) -> list:
        all_links = tag.find_all('a')
        links = [link.get('href', '') for link in all_links]
        return links
    data = [
        {
            'note': parse_text(reference),
            'links': parse_href(reference)
        }
        for reference in references
    ]
    return data


def parse_linkout_category(tag: Tag) -> tuple:
    f_category = lambda x: 'linkout-category' in x.get('class', {})
    category: Optional[Tag] = tag.find(f_category)
    if category is None:
        return tuple()
    category: str = category.text.strip().lower().replace(' ', '-')
    
    category_links: Optional[Tag] = tag.find('ul', {'class': 'linkout-category-links'})
    if category_links is None:
        return tuple()
    category_links: list = category_links.find_all('li')
    parsed_data = [
        {
            'label': link.a.text.strip(),
            'url': link.a.get('href')
        }
        for link in category_links
    ]
    return category, parsed_data


def parse_linkout_section(tag: Optional[Tag]) -> dict:
    if tag is None:
        return dict()
    linkout_list: Optional[Tag] = tag.find('ul', {'class': 'linkout-list'})
    if linkout_list is None:
        return dict()
    linkout_list: list = linkout_list.find_all('li', recursive=False)
    iterator = (  
        parse_linkout_category(linkout) for linkout in linkout_list
    )
    data = {
        item[0]: item[1] for item in iterator if item
    }
    return data


def parse_mesh_terms(tag: Optional[Tag]) -> list:
    if tag is None:
        return []
    keywords_list = tag.find('ul', {'class': 'keywords-list'})
    if keywords_list is None:
        return []
    keywords_list = keywords_list.find_all('li', recursive=False)
    buttons = (
        tag.find('button') for tag in keywords_list
    )
    data: list[str] = [
        button.text.strip() 
        for button in buttons if button is not None
    ]
    return data
    

def parse_article_page(html: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    head = None
    
    main_tag: Optional[Tag] = soup.find('main', {'id': 'article-details'})
    if main_tag is not None:
        head = main_tag.find('header', {'id': 'heading'})
    data: dict = parse_article_head(head)

    abstract_div = soup.find('div', {'id': 'abstract'})
    if abstract_div is not None:
        abstract_div = abstract_div.find('div', {'id': 'enc-abstract'})
        if abstract_div is not None:    
            data['abstract']: str = abstract_div.text.strip()
    
    tag = soup.find('div', {'id': 'similar', 'class': 'similar-articles'})
    data['similar-articles']: list = parse_articles_list(tag)
    
    tag = soup.find('div', {'id': 'citedby'})
    data['cited-by-articles']: list = parse_articles_list(tag)
    
    tag = soup.find('div', {'id': 'references'})
    data['references']: list = parse_references(tag)
    
    tag = soup.find('div', {'id': 'linkout', 'class': 'linkout'})
    data['linkout']: dict = parse_linkout_section(tag)
    
    tag = soup.find('div', {'id': 'mesh-terms'})
    data['mesh-terms']: list = parse_mesh_terms(tag)
    return data


