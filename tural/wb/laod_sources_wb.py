from selenium_pages_wb import UseSelenium

def main():
    url = "https://www.wildberries.ru/catalog/dom-i-dacha/vannaya/polotentsa"

    # Ограничим парсинг первыми 10 страницами
    MAX_PAGE = 1
    i = 1
    while i <= MAX_PAGE:
        filename = f'page_' + str(i) + '.html'
        if i == 1:
            UseSelenium(url, filename).save_page()
        else:
            url_param = url + '?page=' + str(i)
            UseSelenium(url_param, filename).save_page()

        i += 1

if __name__ == '__main__':
    main()