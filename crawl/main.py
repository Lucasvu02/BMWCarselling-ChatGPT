import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import json
from src.utils import get_current_folder


def html_to_json(content, indent=None):
    soup = content
    rows = soup.find_all("tr")

    headers = {}
    thead = soup.find("thead")
    if thead:
        thead = soup.find_all("th")
        for i in range(len(thead)):
            headers[i] = thead[i].text.strip().lower()
    data = []
    for row in rows:
        cells = row.find_all("td")
        if thead:
            items = {}
            if len(cells) > 0:
                for index in headers:
                    items[headers[index]] = cells[index].text
        else:
            items = []
            for index in cells:
                items.append(index.text.strip())
        if items:
            data.append(items)
    return json.dumps(data, indent=indent,ensure_ascii=False)
def extract_from_table(table):
    table_data = []
    for row in table.find_all('tr'):
        raw_data = []
        for cell in row.find_all(['th','td']):
            cell_text = cell.get_text(strip=True)
            colspan = int(cell.get('colspan', 1))
            raw_data.extend([cell_text]*colspan)
        table_data.append(raw_data)
    #print(json.dumps(dict(table_data)))
    return table_data
def extract_table(url,table_class):
    session = requests.Session()
    response = session.get(url)
    soup = BeautifulSoup(response.content,'html.parser')
    table = soup.find('table',class_=table_class)
    return table
def get_information(url):
    session = requests.Session()
    response = session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('span',class_="mw-page-title-main")
    if title == None:
        return ("","")
    information = soup.find('div',class_="mw-body-content")
    text = ""
    text_infor = information.find_all(['p','caption','h2','h3','li','table'])
    for tag in text_infor:
        if tag.name=="table":
            text += tabulate(extract_from_table(tag))
        elif tag.name == "li":
            if tag.text.strip() != "":
                text += "- "+ tag.text +"\n"
        elif tag.name =="h2" or tag.name == "h3":
            text += tag.text + ":\n"
        else:
            text += tag.text + " "
    text = text.split("\n")
    text = "\n".join([x for x in text if x.strip() != "-"])
    text = text.split("References")[0].split("Summary")[0]
    return (title.text,text)
url = "https://en.wikipedia.org/wiki/List_of_BMW_vehicles"
table = extract_table(url,"wikitable")
prefix = "https://en.wikipedia.org/"
th_elements = table.find_all('a')
links = [prefix+link['href'] for link in th_elements]
links = list(set(links))

for link in links[:1]:
    title,text = get_information(links[1])
    print(title)
    print(text)
    with open(get_current_folder()+f"/data/{title}.txt","w",encoding="UTF-8") as f:
        f.write(text)
#a_tags = []
#for th in th_elements:
#    links = th.find_all('a')
#    a_tags.extend([prefix+link['href'] for link in links])
#print(a_tags)