import requests 
from bs4 import BeautifulSoup

url = 'https://www.pichau.com.br/hardware/placa-de-video'

headers = {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}

site = requests.get(url, headers = headers)
soup = BeautifulSoup(site.content, 'html.parser')
placas = soup.find_all('div',class_='MuiCardContent-root jss207')
ultima_pagina = soup.find('span', class_='MuiButtonBase-root MuiPaginationItem-root MuiPaginationItem-page MuiPaginationItem-textPrimary MuiPaginationItem-sizeLarge').get_text().strip()

for i in range(1, int(ultima_pagina)):
    url_pag = f'https://www.pichau.com.br/hardware/placa-de-video?page={i}'
    site = requests.get(url_pag, headers = headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    placas = soup.find_all('div',class_='MuiCardContent-root jss207')

    with open ('precos_placas.csv', 'a',newline='',encoding='UTF8') as f:
        for placa in placas:
            marca = placa.find('a', class_='MuiTypography-root jss221 jss222 MuiTypography-h6').get_text().strip()

            try:
                preco = placa.find('span', class_= 'jss251').get_text().strip()
                num_preco = preco[2:]
                num_preco = num_preco[:-3]
            
            except:
                num_preco = '0'

            try:
                preco_boleto = placa.find('span', class_='jss224').get_text().strip()
                index = preco_boleto(',')
                num_preco_boleto = preco_boleto[10:index]

            except:
                num_preco_boleto = '0'

            linha = marca + ';' + num_preco + ';' + num_preco_boleto + '\n'
            print(linha)
            f.write(linha)

    print(url_pag)