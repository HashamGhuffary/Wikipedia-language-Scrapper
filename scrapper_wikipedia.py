import requests
from bs4 import BeautifulSoup
import csv
url = 'https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes'


def make_request():
    r = requests.get(url)
    html = r.text
    return html


def scrape(html_passed):
    soup = BeautifulSoup(html_passed, 'lxml')

    main_table = soup.find("table", {"id": "Table"})

    # print(main_table)
    row_table = main_table.findAll('tbody')[0]
    list_of_tags = row_table.findAll('tr')
    list_of_tags.remove(list_of_tags[0])

    lang_nick_list = []
    local_names_list = []
    iso_names_list = []
    for i in list_of_tags:
        list_of_all_atrs = []
        for _ in i:
            list_of_all_atrs.append(_)
        iso_name = str(list_of_all_atrs[5])
        soup = BeautifulSoup(iso_name, 'lxml')
        iso_name = soup.text

        local_name = str(list_of_all_atrs[7])
        soup = BeautifulSoup(local_name, 'lxml')
        local_name = soup.text

        lang_nick = str(list_of_all_atrs[9])
        soup = BeautifulSoup(lang_nick, 'lxml')
        lang_nick = soup.text

        lang_nick_list.append(lang_nick)
        local_names_list.append(local_name)
        iso_names_list.append(iso_name)

    return iso_names_list, local_names_list, lang_nick_list


if __name__ == '__main__':
    iso_names, local_names, lang_nicks = scrape(make_request())
    with open('info.csv', 'w') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(['Languages', 'Local names', 'codes'])
        thewriter.writerow([''])

    with open('info.csv', 'a', encoding="utf-8") as f:
        thewriter = csv.writer(f)

        for i, x, _ in zip(iso_names, local_names, lang_nicks):
            thewriter.writerow([i, x, _])
