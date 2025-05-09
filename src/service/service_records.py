import requests
import traceback
from bs4 import BeautifulSoup
from src.model.record import obj_to_record, RecordError
from src.utils.utils import get_proxy, get_user_agent, create_logger, export_csv

session, user_agent = None, None
def find_records_by_category(category_param):
    global session
    global user_agent

    session = requests.session()
    user_agent = get_user_agent()

    soup = get_showcase_page()
    if isinstance(soup, str):
        raise ValueError(soup)

    category_url, category_title = '', ''
    categories = soup.select('div[class="columned-holder"]')
    for category in categories:
        category_el = category.select_one('h4[class="columned-text-title"]')
        category_title = category_el.get_text(strip=True)
        if category_param.lower() in category_title.lower():
            category_el = category.select_one('article a')
            if category_el:
                category_url = category_el.get("href")
            break

    if not category_url:
        raise ValueError(f'Categoria não encontrada {category_param}')

    category_url= f'https://www.guinnessworldrecords.com.br{category_url}'
    soup = get_category_page(category_url)
    if isinstance(soup, str):
        raise ValueError(soup)

    obj_records = []
    records = soup.select('a[class="record-grid-item"]')
    for record in records:
        obj = {}
        record_url = record.get('href')
        record_url = f'https://www.guinnessworldrecords.com.br{record_url}'
        soup = get_record_page(record_url)
        if isinstance(soup, str):
            obj_records.append(RecordError(err= soup))
            continue

        details = soup.select('dl div.equal-one')
        for el in details:
            title_el = el.select_one('dt')
            value_el = el.select_one('dd')
            obj[title_el.get_text(strip=True)] = value_el.get_text(strip=True)

        description = ''
        div_description = soup.select_one('div[id="record-text-content"]')
        if div_description:
            paragraphs = div_description.select('p')
            for p in paragraphs:
                description += p.get_text(strip=True) + ''

        record_title = ''
        header = soup.select_one('header[class="page-title"]')
        if header:
            record_title = header.get_text(strip=True)

        obj['Descricao'] = description
        obj['Titulo'] = record_title
        obj['Categoria'] = category_title
        obj = obj_to_record(obj)
        obj_records.append(obj)
    return obj_records

def get_showcase_page():
    url = 'https://www.guinnessworldrecords.com.br/records/showcase'
    for attempt in range(2):
        try:
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'pt-PT,pt;q=0.9',
                'priority': 'u=0, i',
                'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': user_agent,
            }

            response = session.get(url, headers=headers)
            soup = BeautifulSoup(markup=response.text, features='html.parser' )
            return soup
        except Exception as ex:
            return str(ex)

def get_category_page(url):
    for attempt in range(2):
        try:
            headers = {
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': user_agent,
                'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }

            response = session.get(url, headers=headers)
            soup = BeautifulSoup(markup=response.text, features='html.parser' )
            return soup
        except Exception as ex:
            return str(ex)

def get_record_page(url):
    for attempt in range(2):
        try:
            headers = {
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': user_agent,
                'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }

            response = session.get(url, headers=headers)
            soup = BeautifulSoup(markup=response.text, features='html.parser' )
            return soup
        except Exception as ex:
            return str(ex)

def testeeee():
    res = find_records_by_category("Celebridade")
    pass