import requests
from bs4 import BeautifulSoup
import boto3
import uuid

def lambda_handler(event, context):
    url = "https://coinmarketcap.com/"

    response = requests.get(url)
    if response.status_code != 200:
        return {
            'statusCode': response.status_code,
            'body': 'Error al acceder a la página web'
        }

    soup = BeautifulSoup(response.text, 'html.parser')

    crypto_names = soup.find_all("p", attrs={"class": "sc-65e7f566-0 iPbTJf coin-item-name"})
    crypto_prices = soup.find_all("div", attrs={"class": "sc-b3fc6b7-0 dzgUIj"})
    crypto_marketcap = soup.find_all("span", "sc-11478e5d-1 jfwGHx")
    crypto_vol_24hrs = soup.find_all("p", attrs={"class": "sc-71024e3e-0 bbHOdE font_weight_500"})
    crypto_circulation = soup.find_all("p", attrs={"class": "sc-71024e3e-0 hhmVNu"})

    crypto_name_clear = [i.text for i in crypto_names]
    crypto_price_clear = [i.text for i in crypto_prices]
    crypto_marketcap_clear = [i.text for i in crypto_marketcap]
    crypto_vol_24hrs_clear = [i.text for i in crypto_vol_24hrs]
    crypto_circulation_clear = [i.text for i in crypto_circulation]

    rows = []
    for i in range(len(crypto_name_clear)):
        row = {
            'id': str(uuid.uuid4()),  # Generar un ID único para cada entrada
            'name': crypto_name_clear[i],
            'price': crypto_price_clear[i] if i < len(crypto_price_clear) else 'N/A',
            'marketcap': crypto_marketcap_clear[i] if i < len(crypto_marketcap_clear) else 'N/A',
            'vol_24hrs': crypto_vol_24hrs_clear[i] if i < len(crypto_vol_24hrs_clear) else 'N/A',
            'circulation': crypto_circulation_clear[i] if i < len(crypto_circulation_clear) else 'N/A'
        }
        rows.append(row)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TablaWebScrappingCrypto')

    scan = table.scan()
    with table.batch_writer() as batch:
        for each in scan['Items']:
            batch.delete_item(
                Key={
                    'id': each['id']
                }
            )

    for row in rows:
        table.put_item(Item=row)

    return {
        'statusCode': 200,
        'body': rows
    }