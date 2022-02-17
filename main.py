import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import webbrowser

f = open("output.csv", "w")
f.truncate()
f.close()

brands = ('drops',  'stylecraft', 'dmc', 'drops', 'hahn')
products = ('drops-baby-merino-mix', 'stylecraft-special-dk', 'dmc-natura-xl', 'drops-safran', 'alpacca-speciale')
dict_products = { i : products[i] for i in range(0, len(products) ) }

for brand, product in zip(brands, products):

    website_url = requests.get('https://www.wollplatz.de/wolle/' + brand + '/' + product).text
    r = requests.get('https://www.wollplatz.de/wolle/' + brand + '/' + product)
    print(r.status_code)
    if r.status_code != 404:

        soup = BeautifulSoup(website_url,'html.parser')

        if (soup.find('div', {"class" : 'buy-extrainfo'})) != None:
            old_price = soup.find('span', {'class': 'product-price-amount'})
            print('Old price is ' + old_price.text)


        price = soup.find('span', {'class' : 'product-price'})
        new_price = price.find('span' , {'class' : 'product-price-amount'})
        print('New price ' + new_price.text)
        price_dict = {'Price': new_price.text}

        table_div = soup.find("div", {"id": "pdetailTableSpecs"})

        table = table_div.find("table")
        table_rows = table.find_all('tr')


        data = {}
        for tr in table_rows:
            td = tr.find_all('td')
            if len(td) != 2 : continue
            data[td[0].text] = td[1].text.strip()

        res = dict((k, data[k]) for k in ['Zusammenstellung' , 'Nadelstärke'] if k in data)
        res.update(price_dict)
        product_names = {'Brand': product}
        res.update(product_names)
        data_frame = pd.DataFrame([res], columns=res.keys())
        data_frame.to_csv('output.csv', mode='a', index=False, header=False)

    else:
        print("site not found")


result = pd.read_csv('output.csv', names=["Zusammenstellung", "Nadelstärke", "Price", "Brand"] )
result = result.set_index("Brand")
html = result.to_html()
path = os.path.abspath('result.html')
url = 'file://' + path

with open(path, 'w') as f:
    f.write(html)
webbrowser.open(url)
