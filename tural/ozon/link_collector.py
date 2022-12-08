from bs4 import BeautifulSoup
import glob
#номер 2
#меняем ('div', attrs={'class', 'k5u'})

def get_pages() -> list:
    return glob.glob('C:/PyProjects/poject_1/tural/ozon/pages/*.html')


def get_html(page: str):
    with open(page, 'r', encoding='utf-8') as f:
        return f.read()


def parse_data(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')

    try:
        links = []
        products = soup.find('div', attrs={'class', 'k5u'}).find_all('a')  # k7r
        for product in products:
            links.append(product.get('href').split('?')[0])
    except:
        print('НЕ t6k')
        links = []
        products = soup.find('div', attrs={'class', 'k8t'}).find_all('a')  # k7r
        for product in products:
            links.append(product.get('href').split('?')[0])

        # print('НЕ t6k, k8t')

    #return set(links)
    final_links = []
    min_len = len(links[0])/2
    for link in links:
        if (link not in final_links) and (len(link) > min_len):
            final_links.append(link)

    return final_links[:10]

def main():
    pages = get_pages()

    all_links = []

    for page in pages:
        html = get_html(page)
        links = parse_data(html)
        all_links = all_links + list(links)

    print(all_links)
    print(len(all_links))

    with open(r'C:\PyProjects\poject_1\tural\ozon\product_links.txt', 'w', encoding='utf-8') as f:
        for link in all_links:
            f.write(link + '\n')


if __name__ == '__main__':
    main()