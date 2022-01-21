from bs4 import BeautifulSoup


def parse_int(string: str) -> int:
    integer = int(string.replace(',', ''))
    return integer


def parse_results_amount(table_head) -> int:
    results_amount_div = table_head.find('div', {'class': 'results-amount'})
    results_amount = parse_int(results_amount_div.span.text)
    return results_amount


def parse_total_pages(table_head) -> int:
    pagination_div = table_head.find('div', {'class': 'top-pagination'})
    pagination_label = pagination_div.find('label', {'class': 'of-total-pages'})
    total_pages = parse_int(pagination_label.text.split()[-1])
    return total_pages


def parse_article(article) -> dict:
    article_data = dict()
    article_content = article.find('div', {'class': 'docsum-content'})
    title_tag = article_content.find('a', {'class': 'docsum-title'})

    article_data['href'] = title_tag['href']
    article_data['text'] = title_tag.text
    return article_data


def parse_search_page(html: str) -> dict:
    data = dict()
    soup = BeautifulSoup(html, 'html.parser')
    search_results = soup.find('div', {'id': 'search-results'})

    table_head = search_results.find('div', {'class': 'top-wrapper'})
    data['results_amount'] = parse_results_amount(table_head)
    data['total_pages'] = parse_total_pages(table_head)

    articles_table = search_results.find('div', {'class': 'search-results-chunks'})
    articles = articles_table.find_all('article')
    data['articles'] = [parse_article(article) for article in articles]
    return data
