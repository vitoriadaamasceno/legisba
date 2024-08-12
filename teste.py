import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import ssl
from bs4 import BeautifulSoup as bs



'''
O código fornecido configura uma sessão de requisições HTTP com uma adaptação específica para SSL. 
A classe TLSAdapter é uma subclasse de HTTPAdapter que modifica o contexto SSL para usar um conjunto de cifras específico (DEFAULT@SECLEVEL=1).
Isso pode ser necessário para contornar problemas de compatibilidade SSL/TLS com o servidor.
Essa versao não será mais usada pois mudei a versao do python e da bibiliote urllib3
https://github.com/jessecooper/pyetrade/issues/85 - link da solução

Sobre a camada SSL / TLS:
SSL / TLS O SSL (camada de portas de segurança) permite a comunicação segura entre os lados cliente e servidor de uma aplicação web, por meio de uma confirmação da identidade de um servidor e a verificação do seu nível de confiança. 
Ele age como uma subcamada nos protocolos de comunicação na internet (TCP/IP).
Funciona com a autenticação das partes envolvidas na troca de informações.

'''
url = 'https://www.legislabahia.ba.gov.br/'
class TLSAdapter(HTTPAdapter): # TLSAdapter class cria um certificado SSL default para a sessão
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = context
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount('https://', TLSAdapter())
html = session.get(url)
html = bs(html.content, 'html.parser')
print(html.h1)