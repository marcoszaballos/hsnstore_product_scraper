import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pymysql.cursors

def format_price(price_str):
    if price_str == 'N/A':
        return None
    else:
        return float(price_str.replace('€', '').replace(',', '.'))

def format_discount_percentage(percentage_str):
    if percentage_str == 'N/A':
        return None
    else:
        return float(percentage_str.replace('%', ''))

def get_product_data(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        name = soup.select_one('div.col-xs-12.no-gutter.product-name').text.strip()
    except AttributeError:
        name = 'N/A'
    try:
        discounted_price = format_price(soup.select_one('div.final-price').text.strip())
    except AttributeError:
        discounted_price = None
    try:
        regular_price = format_price(soup.select_one('div[class*="regular-price"]').text.strip())
    except AttributeError:
        regular_price = None
    try:
        discount_percentage = format_discount_percentage(soup.select_one('div.discount-percentage').text.strip())
    except AttributeError:
        discount_percentage = None
    try:
        saving_div = soup.select_one('div.saving')
        saving = format_price(saving_div.find('span').text.strip()) if saving_div else None
    except AttributeError:
        saving = None

    return {
        'name': name,
        'discounted_price': discounted_price,
        'regular_price': regular_price,
        'discount_percentage': discount_percentage,
        'saving': saving
    }

def insert_into_database(product_data, connection):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO scraper_hsn.PRODUCTOS (NAME, DISCOUNTED_PRICE, REGULAR_PRICE, DISCOUNT_PERCENTAGE, SAVING, DATE) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (product_data['name'], product_data['discounted_price'], product_data['regular_price'], product_data['discount_percentage'], product_data['saving'], product_data['date']))
            
        connection.commit()
    except Exception as e:
        print(f"Error al insertar en la base de datos: {e}")

def main():
    today_date = datetime.now().strftime('%Y-%m-%d')

    urls = [
        'https://www.hsnstore.com/marcas/sport-series/evolate-2-0-whey-isolate-cfm-500g-turron',
		'https://www.hsnstore.com/marcas/sport-series/evoclear-hydro-500g-mango',
		'https://www.hsnstore.com/marcas/raw-series/creatina-excell-creapure-500g',
		'https://www.hsnstore.com/marcas/food-series/gourmet-pasta-con-pollo-en-salsa-de-miel-y-especias-400g',
		'https://www.hsnstore.com/marcas/food-series/tableta-chocolate-negro-hiperproteico-con-stevia-sin-azucar-100g',
		'https://www.hsnstore.com/marcas/food-series/salsa-barbacoa-350g',
        'https://www.hsnstore.com/marcas/essential-series/omega-3-aceite-pescado-1000mg-120-perlas',
		'https://www.hsnstore.com/marcas/essential-series/l-teanina-250mg-120-veg-caps',
		'https://www.hsnstore.com/marcas/essential-series/bisglicinato-de-magnesio-175mg-magnesio-120-veg-caps',
		'https://www.hsnstore.com/marcas/essential-series/sleep-care-120-veg-caps',
		'https://www.hsnstore.com/marcas/essential-series/cafeina-200mg-120-tabs'
    ]

    connection = pymysql.connect(host='',
                                 user='',
                                 password='',
                                 database='',
                                 cursorclass=pymysql.cursors.DictCursor)

    for url in urls:
        product_data = get_product_data(url)
        product_data['date'] = today_date 
        insert_into_database(product_data, connection)

    connection.close()

if __name__ == '__main__':
    main()
