import requests
from bs4 import BeautifulSoup

url = "https://coinmarketcap.com/"

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

crypto_names = soup.find_all("p", attrs={"class": "sc-65e7f566-0 iPbTJf coin-item-name"})
crypto_prices = soup.find_all("div", attrs={"class": "sc-b3fc6b7-0 dzgUIj"})
crypto_marketcap = soup.find_all("span", "sc-11478e5d-1 jfwGHx")
crypto_vol_24hrs = soup.find_all("p", attrs={"class": "sc-71024e3e-0 bbHOdE font_weight_500"})
crypto_circulation = soup.find_all("p", attrs={"class":"sc-71024e3e-0 hhmVNu"})

crypto_name_clear = []
crypto_price_clear =  []
crypto_marketcap_clear = []
crypto_vol_24hrs_clear = []
crypto_circulation_clear = []


for i in crypto_names:
    print(i.text)
    crypto_name_clear.append(i.text)

for i in crypto_prices:
    print(i.text)
    crypto_price_clear.append(i.text)

for i in crypto_marketcap:
    print(i.text)
    crypto_marketcap_clear.append(i.text)

for i in crypto_vol_24hrs:
    print(i.text)
    crypto_vol_24hrs_clear.append(i.text)

for i in crypto_circulation:
    print(i.text)
    crypto_circulation_clear.append(i.text)
print("\n")

crypto_data = []
for i in range(len(crypto_name_clear)):
    crypto_info = {
        "name": crypto_name_clear[i],
        "price": crypto_price_clear[i] if i < len(crypto_price_clear) else "N/A",
        "marketcap": crypto_marketcap_clear[i] if i < len(crypto_marketcap_clear) else "N/A",
        "vol_24hrs": crypto_vol_24hrs_clear[i] if i < len(crypto_vol_24hrs_clear) else "N/A",
        "circulation": crypto_circulation_clear[i] if i < len(crypto_circulation_clear) else "N/A"
    }
    crypto_data.append(crypto_info)

for data in crypto_data:
    print(f"\"name\": \"{data['name']}\",")
    print(f"\"price\": \"{data['price']}\",")
    print(f"\"marketcap\": \"{data['marketcap']}\",")
    print(f"\"vol_24hrs\": \"{data['vol_24hrs']}\",")
    print(f"\"circulation\": \"{data['circulation']}\"")
    print()  