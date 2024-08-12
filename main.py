import requests
from bs4 import BeautifulSoup as bs
import re

url = 'https://www.legislabahia.ba.gov.br/'

try:
    html = requests.get(url)
    html.raise_for_status()
except requests.exceptions.RequestException as error:
    print("Ocorreu um erro ao solicitar request, verifique a url e sua conexão :",error)

html = bs(html.content, 'html.parser')

# primeira etapa coletar a tabela e as urls e categorias
try:
  table = html.find('table', {'class': 'table cols-0'})
except AttributeError as error:
    print("Ocorreu um erro ao buscar a tabela, verifique a classe da tabela :",error)
else:
    lines = table.find_all('a')
    urls = []
    categorias = []
    for line in lines:
        url = line.get('href')
        urls.append('https://www.legislabahia.ba.gov.br'+url)
        line = re.search(r'=(\d+)$',url)
        categorias.append(line.group(1))
        
    print(urls)
    print(categorias)