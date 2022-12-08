from selenium_pages import UseSelenium
#номер 1
#меняем ссылку
def main():
    url = "https://www.ozon.ru/category/fotoramki-i-fotoalbomy-14637/"

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