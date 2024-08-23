import requests
import asyncio #tornar o código assíncrono
from bs4 import BeautifulSoup as bs , Tag
import re
import json

url = 'https://www.legislabahia.ba.gov.br/'

def get_html(url):
    try:
        html = requests.get(url)
        html.raise_for_status() 
        html_soup = bs(html.content, 'html.parser')
    except requests.exceptions.RequestException as error:
        print("Ocorreu um erro ao solicitar request, verifique a url e sua conexão :",error)
        return 
    return html_soup


#coletar a tabela e as urls e categorias
def get_urls_table(html, class_table):
    try:
        table = html.find('table', {'class': class_table})
    except AttributeError as error:
        print("Ocorreu um erro ao buscar a tabela, verifique a classe da tabela :",error)
    else:
        lines = table.find_all('a')
        urls = []
        for line in lines:
            url = line.get('href')
            urls.append('https://www.legislabahia.ba.gov.br'+url)
            urls = list(set(urls))
    return urls



#urls_categorias = ['https://www.legislabahia.ba.gov.br/documentos?categoria%5B0%5D=7']
#coletar link dos documentos ainda sem paginação
def get_link_documents(urls_categorias):
    links_documentos = []
    for url in urls_categorias:
        html = get_html(url)
        urls_documentos = get_urls_table(html,'table cols-2')
        for url in urls_documentos:
            links_documentos.append(url)
    
    return links_documentos
            


#url_docs = ['https://www.legislabahia.ba.gov.br/documentos/lei-no-14764-de-14-de-agosto-de-2024','https://www.legislabahia.ba.gov.br/documentos/lei-no-14763-de-14-de-agosto-de-2024']
# extrair dados dos documentos
def extrair_dados_documentos(url_docs):
    dados = []
    for url in url_docs:
        try:
            html = get_html(url)
        except AttributeError as error:
            print("Ocorreu um erro ao buscar a documento :",error)    
        else:
            if html:
                    label = html.find_all('div', {'class': 'field--label'})
                    value = html.find_all('div', {'class': 'field--item'})
                    text = html.find_all('div', {'class': 'field field--name-body field--type-text-with-summary field--label-hidden field--item'})
                    dado = {}
                    for i in range(len(label)):
                        dado[label[i].text] = value[i].text 
                    #dado['Texto'] = text[0].text
                    dados.append(dado)         
    return dados


def emit_json(filename, dados):
    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(dados, json_file, ensure_ascii=False, indent=4)         

            

def main():
    html = get_html(url)
    url_categorias = get_urls_table(html,'table cols-0')
    url_docs =get_link_documents(url_categorias)
    dados  = extrair_dados_documentos(url_docs)
    emit_json('dados.json',dados) 
    
if __name__ == '__main__':
    main()

        